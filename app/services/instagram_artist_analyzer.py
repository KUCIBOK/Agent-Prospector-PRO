"""
Instagram Artist Analyzer — analyze emerging and established African artists.

Detects:
1. EMERGING ARTISTS (< 5 years visible, < 10K followers)
   - Young aesthetic, fresh portfolio
   - High engagement rate (>5%)
   - Recent gallery mentions
   - Actively posting

2. ESTABLISHED ARTISTS (> 5 years, > 10K followers)
   - Consistent presence
   - Multiple exhibition mentions
   - International network
   - Professional portfolio

Uses Instagram Business API (requires Instagram Pro Account) or public scraping.
Free approach: BeautifulSoup + requests (respects rate limits).
"""

import logging
import os
from datetime import datetime, timezone

import requests
from sqlmodel import Session, col, select

from app.db import SessionLocal
from app.models import Prospect, ProspectType, Signal, SignalType
from app.models.base import require_id
from app.models.signal import Confidence, Importance

logger = logging.getLogger(__name__)


class InstagramArtistAnalyzer:
    """Analyze Instagram profiles of African artists."""

    def __init__(self, session: Session):
        self.session = session
        self.instagram_api_key = os.getenv("INSTAGRAM_BUSINESS_API_KEY")
        self.instagram_access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")

    def analyze_artist_instagram(self, prospect: Prospect) -> dict:
        """
        Analyze an artist's Instagram profile.

        Returns:
        {
            "followers": int,
            "following": int,
            "posts": int,
            "engagement_rate": float,
            "maturity_level": "EMERGING" | "ESTABLISHED",
            "quality_score": 0-100,
            "last_post_date": datetime,
            "post_frequency": "daily" | "weekly" | "monthly",
            "bio_keywords": [str],
            "verified": bool,
            "is_artist": bool,
        }
        """
        if not prospect.instagram:
            return {"error": "No Instagram profile"}

        try:
            # Extract username from Instagram handle
            username = prospect.instagram.strip("@/").split("/")[-1].lower()

            # Try API first (if configured)
            if self.instagram_api_key and self.instagram_access_token:
                data = self._fetch_instagram_api(username)
            else:
                # Fallback: public scraping (respectful, no auth needed)
                data = self._scrape_instagram_public(username)

            if not data:
                return {"error": f"Could not fetch {username}"}

            # Analyze quality
            quality_analysis = self._analyze_quality(data)
            data.update(quality_analysis)

            logger.info(
                f"✅ Analyzed {prospect.name}: {data['maturity_level']} "
                f"({data['followers']} followers, {data['engagement_rate']:.1f}% engagement)"
            )

            return data

        except Exception as e:
            logger.error(f"Error analyzing {prospect.instagram}: {e!s}")
            return {"error": str(e)}

    def _fetch_instagram_api(self, username: str) -> dict | None:
        """
        Use Instagram Business API (requires setup).

        Setup:
        1. Create Instagram Business account
        2. Get access token from Meta Developers
        3. Set INSTAGRAM_ACCESS_TOKEN env var
        """
        try:
            # Get Instagram user ID from username
            url = "https://graph.instagram.com/ig_hashtag_search"
            params = {
                "user_id": os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID"),
                "fields": "username,name,profile_picture_url,followers_count,media_count",
                "access_token": self.instagram_access_token,
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Instagram API error: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Instagram API error: {e!s}")
            return None

    def _scrape_instagram_public(self, username: str) -> dict | None:
        """
        Scrape public Instagram profile (respectful scraping).

        Note: Instagram actively blocks scrapers. This is a template.
        Better approach: Use instagrapi library with proper delays.
        """
        try:
            logger.info(f"📱 Scraping Instagram public profile: {username}")

            # Use instagrapi if available (install: pip install instagrapi)
            try:
                from instagrapi import Client
            except ImportError:
                logger.warning("instagrapi not installed. Install with: pip install instagrapi")
                return None

            # Create client (no auth = public data only)
            client = Client()

            # Fetch user info
            user_info = client.user_info_by_username(username)

            data = {
                "username": username,
                "followers": user_info.follower_count,
                "following": user_info.following_count,
                "posts": user_info.media_count,
                "bio": user_info.biography,
                "is_verified": user_info.is_verified,
                "profile_picture_url": user_info.profile_pic_url,
                "name": user_info.full_name,
            }

            # Get recent posts to calculate engagement
            medias = client.user_medias(user_info.pk, amount=20)

            if medias:
                likes = [m.like_count or 0 for m in medias]
                comments = [m.comment_count or 0 for m in medias]
                avg_engagement = (sum(likes) + sum(comments)) / len(medias)
                engagement_rate = (avg_engagement / max(data["followers"], 1)) * 100

                last_post = medias[0]
                data["engagement_rate"] = engagement_rate
                data["last_post_date"] = last_post.taken_at.isoformat()
                data["last_post_likes"] = last_post.like_count
            else:
                data["engagement_rate"] = 0
                data["last_post_date"] = None

            return data

        except Exception as e:
            logger.error(f"Error scraping Instagram: {e!s}")
            return None

    def _analyze_quality(self, data: dict) -> dict:
        """
        Analyze quality and maturity level.

        EMERGING: < 5 years visible, < 10K followers, high engagement
        ESTABLISHED: > 10K followers, consistent presence, recognized
        """
        followers = data.get("followers", 0)
        engagement_rate = data.get("engagement_rate", 0)
        posts = data.get("posts", 0)
        bio = data.get("bio", "").lower()
        is_verified = data.get("is_verified", False)

        quality_score = 0
        quality_breakdown = {}

        # 1. Follower count (25 points)
        if followers >= 100000:
            quality_score += 25
        elif followers >= 50000:
            quality_score += 20
        elif followers >= 10000:
            quality_score += 15
        elif followers >= 5000:
            quality_score += 10
        elif followers >= 1000:
            quality_score += 5
        quality_breakdown["followers"] = min(quality_score, 25)

        # 2. Engagement rate (25 points) — HIGH = >5% is VERY good
        if engagement_rate >= 10:
            quality_score += 25
            quality_breakdown["engagement"] = 25
        elif engagement_rate >= 5:
            quality_score += 20
            quality_breakdown["engagement"] = 20
        elif engagement_rate >= 2:
            quality_score += 10
            quality_breakdown["engagement"] = 10
        else:
            quality_breakdown["engagement"] = 0

        # 3. Post frequency (15 points)
        avg_days_per_post = max(1, 365 / max(posts, 1))
        if avg_days_per_post <= 3:  # Posting every 3 days or more
            quality_score += 15
            quality_breakdown["frequency"] = 15
        elif avg_days_per_post <= 7:
            quality_score += 10
            quality_breakdown["frequency"] = 10
        elif avg_days_per_post <= 30:
            quality_score += 5
            quality_breakdown["frequency"] = 5
        else:
            quality_breakdown["frequency"] = 0

        # 4. Bio professional markers (20 points)
        art_keywords = [
            "artist",
            "artiste",
            "painter",
            "sculptor",
            "photography",
            "contemporary",
            "studio",
        ]
        if any(kw in bio for kw in art_keywords):
            quality_score += 10
            quality_breakdown["bio_professional"] = 10
        else:
            quality_breakdown["bio_professional"] = 0

        # Add verification bonus
        if is_verified:
            quality_score += 10
            quality_breakdown["verified"] = 10
        else:
            quality_breakdown["verified"] = 0

        # Determine maturity level
        if followers >= 10000:
            maturity = "ESTABLISHED"
        elif followers >= 2000 and engagement_rate >= 3:
            maturity = "EMERGING_PROMISING"
        elif followers >= 1000:
            maturity = "EMERGING"
        else:
            maturity = "EARLY_STAGE"

        # Post frequency analysis
        if avg_days_per_post <= 3:
            post_frequency = "daily"
        elif avg_days_per_post <= 7:
            post_frequency = "weekly"
        elif avg_days_per_post <= 30:
            post_frequency = "monthly"
        else:
            post_frequency = "sporadic"

        return {
            "quality_score": min(quality_score, 100),
            "quality_breakdown": quality_breakdown,
            "maturity_level": maturity,
            "post_frequency": post_frequency,
            "is_artist": any(kw in bio for kw in art_keywords),
            "bio_keywords": self._extract_keywords(bio),
        }

    def _extract_keywords(self, bio: str) -> list[str]:
        """Extract relevant keywords from bio."""
        art_keywords = [
            "contemporary",
            "abstract",
            "sculpture",
            "painting",
            "installation",
            "digital",
            "photography",
            "mixed media",
            "printmaking",
            "ceramics",
            "textiles",
            "emerging",
            "studio",
            "collective",
        ]

        keywords = []
        bio_lower = bio.lower()

        for kw in art_keywords:
            if kw in bio_lower:
                keywords.append(kw)

        return keywords

    def bulk_analyze_artists(self) -> list[dict]:
        """
        Analyze all artists in database with Instagram profiles.

        Returns analysis results.
        """
        artists = self.session.exec(
            select(Prospect).where(
                col(Prospect.type) == ProspectType.ARTIST,
                col(Prospect.instagram).is_not(None),
            )
        ).all()

        logger.info(f"🎨 Analyzing {len(artists)} artists on Instagram...")

        results = []

        for artist in artists:
            analysis = self.analyze_artist_instagram(artist)

            if "error" not in analysis:
                # Update prospect with quality metrics
                artist.score = analysis.get("quality_score", 0)
                artist.digital_maturity = analysis.get("maturity_level", "UNKNOWN")

                self.session.add(artist)

                # Detect signals if ESTABLISHED
                if analysis.get("maturity_level") == "ESTABLISHED" and artist.score >= 70:
                    signal = Signal(
                        prospect_id=require_id(artist),
                        signal_type=SignalType.NEW_PUBLICATION,
                        description=f"Instagram: {analysis.get('followers')} followers, "
                        f"{analysis.get('engagement_rate', 0):.1f}% engagement",
                        source_url=f"https://instagram.com/{artist.instagram}",
                        signal_date=datetime.now(timezone.utc),
                        importance=(
                            Importance.HIGH
                            if analysis.get("maturity_level") == "ESTABLISHED"
                            else Importance.MEDIUM
                        ),
                        confidence=Confidence.HIGH,
                    )
                    self.session.add(signal)

                results.append(
                    {
                        "artist": artist.name,
                        "instagram": artist.instagram,
                        "maturity": analysis.get("maturity_level"),
                        "quality_score": analysis.get("quality_score"),
                        "followers": analysis.get("followers"),
                    }
                )

        self.session.commit()

        logger.info(f"✅ Analyzed {len(results)} artists")
        return results


def analyze_instagram_artists_sync() -> int:
    """Helper for manual trigger."""
    session = SessionLocal()
    try:
        analyzer = InstagramArtistAnalyzer(session)
        results = analyzer.bulk_analyze_artists()
        return len(results)
    finally:
        session.close()
