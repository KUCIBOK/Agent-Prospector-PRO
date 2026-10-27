"""
LinkedIn Curator Finder — discover and monitor curators/art advisors.

Uses Proxycurl API (free tier: 100 calls/month) or manual search for:
- Art advisors
- Museum curators
- Gallery directors
- Collectors
- Event organizers (biennales, art fairs)

Monitors for:
- Title changes
- Company changes
- New endorsements
- Profile updates
"""

import logging
import os
from typing import Optional, List
from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select
import requests

from app.models import Prospect, ProspectType, Signal, SignalType
from app.db import SessionLocal

logger = logging.getLogger(__name__)


class LinkedInCuratorFinder:
    """Discover and monitor LinkedIn curators/advisors."""

    def __init__(self, session: Session):
        self.session = session
        # Proxycurl API key (get free at https://proxycurl.com)
        self.proxycurl_api_key = os.getenv("PROXYCURL_API_KEY")
        self.proxycurl_endpoint = "https://napi.proxycurl.com/v2/linkedin"

    def discover_curators_manual_search(self, keywords: List[str]) -> List[dict]:
        """
        Manual search strategy using free sources (no API key needed).

        Search for:
        - "art advisor" + region
        - "curator" + "contemporary art"
        - "galerie" + "directeur"
        - Etc.

        Returns list of discovered prospects.
        """
        logger.info(f"🔍 Manual curator search for keywords: {keywords}")

        discovered = []

        # Strategy: Search LinkedIn URLs in Google
        # "art advisor" site:linkedin.com/in + region
        # But we can't automate this without API

        # For now: return template for manual enrichment
        for keyword in keywords:
            prospect_template = {
                "type": ProspectType.ART_ADVISOR,
                "search_keyword": keyword,
                "name": "[TO_RESEARCH]",
                "linkedin": "[TO_ENRICH]",
                "country": "[TO_ENRICH]",
                "description": f"Found via search: {keyword}",
            }
            discovered.append(prospect_template)

        logger.info(f"📋 Found {len(discovered)} curator profiles to research")
        return discovered

    def discover_curators_from_proxycurl(self) -> List[dict]:
        """
        Use Proxycurl API to search for curators (requires API key).

        Free tier allows 100 searches/month.
        Endpoint: https://napi.proxycurl.com/v2/linkedin/profile/search

        Returns list of curator profiles.
        """
        if not self.proxycurl_api_key:
            logger.warning("⚠️  PROXYCURL_API_KEY not set. Set it to enable LinkedIn API search.")
            return []

        headers = {"Authorization": f"Bearer {self.proxycurl_api_key}"}

        # Search keywords for curators
        search_queries = [
            "art advisor contemporary art",
            "museum curator African art",
            "gallery director international",
            "art consultant emerging markets",
            "collections manager contemporary",
        ]

        discovered = []

        for query in search_queries:
            try:
                logger.info(f"🔎 Proxycurl search: {query}")

                response = requests.get(
                    f"{self.proxycurl_endpoint}/profile/search",
                    headers=headers,
                    params={"search_query": query, "page_size": 10},
                    timeout=10,
                )

                if response.status_code == 200:
                    data = response.json()
                    profiles = data.get("profiles", [])

                    for profile in profiles:
                        prospect = {
                            "type": ProspectType.ART_ADVISOR,
                            "name": profile.get("name"),
                            "linkedin": profile.get("linkedin_profile_url"),
                            "headline": profile.get("headline"),
                            "country": profile.get("country"),
                            "current_company": profile.get("current_company"),
                            "description": profile.get("summary"),
                        }
                        discovered.append(prospect)

                else:
                    logger.warning(f"Proxycurl search failed: {response.status_code}")

            except Exception as e:
                logger.error(f"Error searching Proxycurl: {str(e)}")

        logger.info(f"✅ Proxycurl: discovered {len(discovered)} curator profiles")
        return discovered

    def monitor_linkedin_changes(self) -> List[Signal]:
        """
        Monitor existing LinkedIn profiles for changes.

        Requires Proxycurl profile scraping endpoint.
        """
        signals = []

        # Get all prospects with LinkedIn URLs
        prospects = self.session.exec(
            select(Prospect).where(
                (Prospect.linkedin != None)
                & (Prospect.type.in_([ProspectType.ART_ADVISOR, ProspectType.CURATOR]))
            )
        ).all()

        logger.info(f"📊 Monitoring {len(prospects)} LinkedIn profiles for changes...")

        for prospect in prospects:
            if not self.proxycurl_api_key:
                continue

            try:
                # Fetch fresh profile data from Proxycurl
                profile_data = self._fetch_linkedin_profile(prospect.linkedin)

                if not profile_data:
                    continue

                # Check for title change
                new_title = profile_data.get("headline", "")
                if new_title and prospect.description != new_title:
                    signal = Signal(
                        prospect_id=prospect.id,
                        signal_type=SignalType.CAREER_CHANGE,
                        description=f"Title updated: {new_title}",
                        source_url=prospect.linkedin,
                        signal_date=datetime.now(timezone.utc),
                        importance="HIGH",
                        confidence="HIGH",
                    )
                    signals.append(signal)
                    logger.info(f"🔄 Title change detected for {prospect.name}: {new_title}")

                # Check for company change
                new_company = profile_data.get("current_company", {}).get("name")
                if new_company and prospect.specialty != new_company:
                    signal = Signal(
                        prospect_id=prospect.id,
                        signal_type=SignalType.CAREER_CHANGE,
                        description=f"Now at: {new_company}",
                        source_url=prospect.linkedin,
                        signal_date=datetime.now(timezone.utc),
                        importance="MEDIUM",
                        confidence="HIGH",
                    )
                    signals.append(signal)
                    logger.info(f"🏢 Company change detected for {prospect.name}: {new_company}")

                # Check for recent connections (hiring spree signal)
                recent_connections = profile_data.get("connections_count", 0)
                if recent_connections > 500:
                    signal = Signal(
                        prospect_id=prospect.id,
                        signal_type=SignalType.HIRING_SPREE,
                        description=f"Active networker: {recent_connections} LinkedIn connections",
                        source_url=prospect.linkedin,
                        signal_date=datetime.now(timezone.utc),
                        importance="MEDIUM",
                        confidence="MEDIUM",
                    )
                    signals.append(signal)

            except Exception as e:
                logger.error(f"Error monitoring {prospect.name}: {str(e)}")

        # Save signals
        for signal in signals:
            self.session.add(signal)

        if signals:
            self.session.commit()
            logger.info(f"✅ LinkedIn monitoring: {len(signals)} changes detected")

        return signals

    def _fetch_linkedin_profile(self, linkedin_url: str) -> Optional[dict]:
        """
        Fetch LinkedIn profile data via Proxycurl API.

        Requires PROXYCURL_API_KEY environment variable.
        """
        if not self.proxycurl_api_key:
            return None

        headers = {"Authorization": f"Bearer {self.proxycurl_api_key}"}

        try:
            response = requests.get(
                f"{self.proxycurl_endpoint}/profile",
                headers=headers,
                params={"url": linkedin_url},
                timeout=10,
            )

            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Proxycurl fetch failed for {linkedin_url}: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Error fetching LinkedIn profile: {str(e)}")
            return None

    def enrich_prospect_from_linkedin(self, prospect: Prospect) -> bool:
        """
        Enrich prospect data from their LinkedIn profile.

        Returns True if enrichment successful.
        """
        if not prospect.linkedin or not self.proxycurl_api_key:
            return False

        try:
            profile_data = self._fetch_linkedin_profile(prospect.linkedin)

            if not profile_data:
                return False

            # Update prospect with LinkedIn data
            if profile_data.get("headline"):
                prospect.description = profile_data["headline"]

            if profile_data.get("summary"):
                prospect.description = prospect.description or profile_data["summary"]

            if profile_data.get("country"):
                prospect.country = profile_data["country"]

            if profile_data.get("city"):
                prospect.city = profile_data["city"]

            # Track Africa interest from description
            africa_keywords = ["africa", "african", "emerging market", "contemporary art"]
            if prospect.description:
                desc_lower = prospect.description.lower()
                if any(keyword in desc_lower for keyword in africa_keywords):
                    prospect.africa_interest = "MEDIUM"

            self.session.add(prospect)
            self.session.commit()

            logger.info(f"✅ Enriched {prospect.name} from LinkedIn")
            return True

        except Exception as e:
            logger.error(f"Error enriching prospect from LinkedIn: {str(e)}")
            return False


def discover_linkedin_curators_sync(use_api: bool = False) -> int:
    """Helper for manual trigger."""
    session = SessionLocal()
    try:
        finder = LinkedInCuratorFinder(session)

        if use_api and os.getenv("PROXYCURL_API_KEY"):
            curators = finder.discover_curators_from_proxycurl()
        else:
            curators = finder.discover_curators_manual_search([
                "art advisor contemporary",
                "museum curator Africa",
                "gallery director international",
            ])

        # TODO: Save discovered curators to DB
        logger.info(f"🎯 Discovered {len(curators)} curators")

        # Monitor changes
        signals = finder.monitor_linkedin_changes()
        logger.info(f"📊 Found {len(signals)} profile changes")

        return len(curators)

    finally:
        session.close()
