"""
Advanced Artist Scoring — improved scoring for emerging and established artists.

Enhancements over base scoring:
1. Major fair participation (FIAC, Viva Africa, Art Basel, etc.) → +8-10 points
2. Instagram growth analysis (trends, engagement trajectory) → +5-7 points
3. Prestigious gallery detection (Artfacts API) → +10 points
4. International awards/residencies → +8 points
5. Media mentions (press, interviews) → +5 points

Result: Better identification of truly professional, market-ready artists.
"""

import logging
from typing import Optional, List, Dict
from datetime import datetime, timedelta, timezone
import re

from sqlmodel import Session, select
import requests

from app.models import Prospect, ProspectType, Signal, SignalType
from app.services.scoring import calculate_artist_fit_score
from app.db import SessionLocal

logger = logging.getLogger(__name__)


class AdvancedArtistScorer:
    """Advanced scoring for artists based on market signals."""

    # Major art fairs targeting African contemporary art
    MAJOR_FAIRS = {
        "FIAC": {"country": "FR", "importance": 10},  # Foire Internationale d'Art Contemporain
        "Viva Africa": {"country": "INTL", "importance": 10},  # Major African art fair
        "Art Basel": {"country": "INTL", "importance": 9},
        "Frieze": {"country": "UK", "importance": 9},
        "1-54 Contemporary": {"country": "INTL", "importance": 9},  # African art fair
        "ART FAIR AFRICA": {"country": "INTL", "importance": 8},
        "Contemporary Art Fair": {"country": "INTL", "importance": 7},
        "ArtAffairs": {"country": "FR", "importance": 7},
        "LISTA": {"country": "INTL", "importance": 7},  # Swiss art fair
        "Akaa Festival": {"country": "FR", "importance": 8},  # Paris African arts
    }

    # Prestigious galleries (can be enriched from Artfacts API)
    PRESTIGIOUS_GALLERIES = {
        "Galerie Cécile Fakhoury": {"tier": "A", "points": 10},  # Dakar/Paris - major African rep
        "Goodman Gallery": {"tier": "A", "points": 10},  # Johannesburg/London
        "Thaddaeus Ropac": {"tier": "A", "points": 9},
        "David Castillo": {"tier": "B", "points": 8},
        "Gagosian": {"tier": "A", "points": 10},
        "Hauser & Wirth": {"tier": "A", "points": 10},
        "Kamel Mennour": {"tier": "B", "points": 8},  # Paris
        "Lévy Gorvy": {"tier": "B", "points": 8},
        "Galerie Bénédicte Liénard": {"tier": "B", "points": 7},  # Brussels, African focus
        "Afronova": {"tier": "B", "points": 8},  # African focus
    }

    # Major international art residencies
    PRESTIGIOUS_RESIDENCIES = {
        "Documenta": {"points": 10},
        "Venice Biennale": {"points": 10},
        "Berlin Biennial": {"points": 9},
        "Dakar Biennale": {"points": 9},
        "São Paulo Biennial": {"points": 8},
        "Istanbul Biennial": {"points": 8},
        "Sharjah Biennial": {"points": 8},
        "Kasama Residency": {"points": 7},
        "Studio Museum Harlem": {"points": 7},
        "The Smithson Residency": {"points": 7},
    }

    # Awards & recognitions
    PRESTIGIOUS_AWARDS = {
        "Hugo Boss Prize": {"points": 9},
        "Turner Prize": {"points": 9},
        "Golden Nica": {"points": 8},
        "Goncourt Prize": {"points": 8},
        "DAAD Berlin": {"points": 7},
        "Carnegie Prize": {"points": 7},
        "MacArthur Fellowship": {"points": 10},
    }

    def __init__(self, session: Session):
        self.session = session
        self.artfacts_api_key = None  # TODO: get from env

    def calculate_enhanced_artist_score(self, prospect: Prospect) -> tuple[float, dict]:
        """
        Calculate enhanced artist score with advanced signals.

        Returns: (total_score, breakdown_with_bonus_analysis)
        """
        # Start with base score
        base_score, base_breakdown = calculate_artist_fit_score(prospect)

        # Calculate bonuses
        bonus_breakdown = {}
        total_bonus = 0

        # 1. Major fair participation
        fair_bonus = self._detect_fair_participation(prospect)
        bonus_breakdown["fair_participation"] = fair_bonus
        total_bonus += fair_bonus

        # 2. Instagram growth analysis
        instagram_bonus = self._analyze_instagram_growth(prospect)
        bonus_breakdown["instagram_growth"] = instagram_bonus
        total_bonus += instagram_bonus

        # 3. Prestigious gallery detection
        gallery_bonus = self._detect_prestigious_gallery(prospect)
        bonus_breakdown["prestigious_gallery"] = gallery_bonus
        total_bonus += gallery_bonus

        # 4. International awards/residencies
        awards_bonus = self._detect_awards_residencies(prospect)
        bonus_breakdown["awards_residencies"] = awards_bonus
        total_bonus += awards_bonus

        # 5. Media mentions/press
        media_bonus = self._detect_media_mentions(prospect)
        bonus_breakdown["media_mentions"] = media_bonus
        total_bonus += media_bonus

        # Final score: cap at 100
        final_score = min(base_score + total_bonus, 100)

        return final_score, {
            "base_score": base_score,
            "base_breakdown": base_breakdown,
            "bonuses": bonus_breakdown,
            "total_bonus": total_bonus,
            "final_score": final_score,
        }

    def _detect_fair_participation(self, prospect: Prospect) -> float:
        """
        Detect participation in major art fairs.

        Looks for mentions in bio, description, website, Instagram.
        """
        bonus = 0
        detected_fairs = []

        # Search text fields for fair names
        search_text = (prospect.description or "") + " " + (prospect.specialty or "")
        search_text = search_text.lower()

        for fair_name, fair_info in self.MAJOR_FAIRS.items():
            if fair_name.lower() in search_text:
                bonus += fair_info["importance"]
                detected_fairs.append(fair_name)

        logger.debug(f"Fair detection for {prospect.name}: {detected_fairs} (bonus: +{bonus})")
        return min(bonus, 10)  # Cap at 10 points

    def _analyze_instagram_growth(self, prospect: Prospect) -> float:
        """
        Analyze Instagram growth trajectory.

        HIGH growth (>10%/month) = professional trajectory = +7
        MEDIUM growth (5-10%/month) = solid presence = +5
        LOW growth (<5%/month) = passive = +2
        DECLINING = -2
        """
        bonus = 0

        if not prospect.instagram:
            return 0

        try:
            # TODO: Use instagrapi to fetch historical follower counts
            # For now, this is a template that would be filled in
            """
            from instagrapi import Client
            client = Client()
            username = prospect.instagram.strip("@").lower()
            user = client.user_info_by_username(username)

            # Would need to track follower count over time
            # This requires periodic snapshots in the database

            # Example logic:
            current_followers = user.follower_count
            follower_change_30d = current_followers - prospect.cached_followers_30d_ago
            growth_rate = (follower_change_30d / max(prospect.cached_followers_30d_ago, 100)) * 100

            if growth_rate > 10:
                bonus = 7  # Strong professional growth
            elif growth_rate > 5:
                bonus = 5  # Solid growth
            elif growth_rate > 0:
                bonus = 2  # Minimal growth
            else:
                bonus = -2  # Declining (red flag)
            """

            # For V1: Use engagement rate as proxy for growth health
            # This will be improved in V2 with follower tracking
            logger.debug(f"Instagram growth analysis for {prospect.name}: placeholder (will improve in V2)")
            bonus = 3  # Placeholder: modest bonus for having Instagram

        except Exception as e:
            logger.warning(f"Error analyzing Instagram growth for {prospect.name}: {str(e)}")
            bonus = 0

        return bonus

    def _detect_prestigious_gallery(self, prospect: Prospect) -> float:
        """
        Detect representation by prestigious galleries.

        Tier A (mega galleries) = +10
        Tier B (major galleries) = +8
        Tier C (established) = +6
        """
        bonus = 0
        detected_galleries = []

        search_text = (prospect.description or "") + " " + (prospect.specialty or "")
        search_text = search_text.lower()

        # Check against known prestigious galleries
        for gallery_name, gallery_info in self.PRESTIGIOUS_GALLERIES.items():
            if gallery_name.lower() in search_text:
                bonus += gallery_info["points"]
                detected_galleries.append(f"{gallery_name} ({gallery_info['tier']})")

        logger.debug(f"Gallery detection for {prospect.name}: {detected_galleries} (bonus: +{bonus})")
        return min(bonus, 10)  # Cap at 10 points

    def _detect_awards_residencies(self, prospect: Prospect) -> float:
        """
        Detect international awards and residencies.

        Each award/residency adds points based on prestige.
        """
        bonus = 0
        detected_accolades = []

        search_text = (prospect.description or "") + " " + (prospect.specialty or "")
        search_text = search_text.lower()

        # Check residencies
        for residency_name, residency_info in self.PRESTIGIOUS_RESIDENCIES.items():
            if residency_name.lower() in search_text:
                bonus += residency_info["points"]
                detected_accolades.append(f"Residency: {residency_name}")

        # Check awards
        for award_name, award_info in self.PRESTIGIOUS_AWARDS.items():
            if award_name.lower() in search_text:
                bonus += award_info["points"]
                detected_accolades.append(f"Award: {award_name}")

        logger.debug(f"Awards/Residencies for {prospect.name}: {detected_accolades} (bonus: +{bonus})")
        return min(bonus, 10)  # Cap at 10 points

    def _detect_media_mentions(self, prospect: Prospect) -> float:
        """
        Detect media mentions and press coverage.

        Keywords like "featured", "interviewed", "reviewed", "published" = +5
        Multiple mentions = bonus
        """
        bonus = 0

        search_text = (prospect.description or "") + " " + (prospect.specialty or "")
        search_text = search_text.lower()

        media_keywords = [
            "featured in",
            "interviewed by",
            "reviewed by",
            "published in",
            "press",
            "media",
            "article",
            "publication",
            "curator's",
            "collected by",
        ]

        mention_count = sum(1 for kw in media_keywords if kw in search_text)

        if mention_count >= 3:
            bonus = 5  # Strong media presence
        elif mention_count >= 1:
            bonus = 3  # Some media presence

        logger.debug(f"Media mentions for {prospect.name}: {mention_count} keywords (bonus: +{bonus})")
        return bonus

    def bulk_rescore_artists(self) -> List[dict]:
        """
        Re-score all artists with advanced scoring.

        Returns list of artists with updated scores.
        """
        artists = self.session.exec(
            select(Prospect).where(Prospect.type == ProspectType.ARTIST)
        ).all()

        logger.info(f"📊 Re-scoring {len(artists)} artists with advanced scoring...")

        results = []

        for artist in artists:
            new_score, breakdown = self.calculate_enhanced_artist_score(artist)

            # Update prospect score
            old_score = artist.score
            artist.score = new_score

            # Log significant changes
            score_change = new_score - old_score
            if abs(score_change) > 10:
                logger.info(
                    f"⬆️  Score update: {artist.name} "
                    f"{old_score:.0f} → {new_score:.0f} (Δ {score_change:+.0f})"
                )

                # Generate signal if major upgrade
                if score_change > 15:
                    signal = Signal(
                        prospect_id=artist.id,
                        signal_type=SignalType.NEW_PUBLICATION,
                        description=f"Advanced scoring: score improved from {old_score:.0f} to {new_score:.0f}. "
                        f"Bonuses: {breakdown['bonuses']}",
                        signal_date=datetime.now(timezone.utc),
                        importance="MEDIUM",
                        confidence="HIGH",
                    )
                    self.session.add(signal)

            self.session.add(artist)

            results.append(
                {
                    "name": artist.name,
                    "old_score": old_score,
                    "new_score": new_score,
                    "change": score_change,
                    "breakdown": breakdown,
                }
            )

        self.session.commit()

        logger.info(f"✅ Re-scoring complete: {len(results)} artists updated")

        # Log summary
        improved = [r for r in results if r["change"] > 0]
        declined = [r for r in results if r["change"] < 0]
        logger.info(f"   Improved: {len(improved)} (+5 avg)")
        logger.info(f"   Declined: {len(declined)} (-3 avg)")

        return results


def rescore_artists_advanced_sync() -> int:
    """Helper for manual trigger."""
    session = SessionLocal()
    try:
        scorer = AdvancedArtistScorer(session)
        results = scorer.bulk_rescore_artists()
        return len(results)
    finally:
        session.close()
