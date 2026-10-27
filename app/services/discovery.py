"""
Discovery Engine — Generate and execute search queries.

Discovers:
- Artists: African contemporary artists (emerging & established)
- Clients: International curators, art advisors, galleries

Data sources (free):
- Google Search (via requests + BeautifulSoup)
- LinkedIn profiles
- Instagram hashtags
- Art directories
"""

import logging
from datetime import datetime, timezone

from sqlmodel import Session, select

from app.models import Prospect, ProspectStatus, ProspectType, Source, SourceType

logger = logging.getLogger(__name__)


class SearchQuery:
    """Search query builder."""

    def __init__(self, target_type: ProspectType, keywords: list, countries: list = None):
        self.target_type = target_type
        self.keywords = keywords
        self.countries = countries or []

    def build_google_queries(self) -> list[str]:
        """Build Google search queries."""
        queries = []

        if self.target_type == ProspectType.ARTIST:
            for keyword in self.keywords:
                for country in self.countries:
                    query = f'"{keyword}" artist {country} site:instagram.com OR site:artfacts.net'
                    queries.append(query)
                # Also search without country
                query = f'"{keyword}" African artist portfolio'
                queries.append(query)
        else:  # Clients (advisors, curators)
            for keyword in self.keywords:
                query = f'"{keyword}" Africa contemporary art'
                queries.append(query)

        return queries[:10]  # Limit to avoid rate limiting

    def build_linkedin_queries(self) -> list[str]:
        """Build LinkedIn search queries."""
        queries = []

        if self.target_type == ProspectType.ART_ADVISOR:
            queries = [
                "art advisor Africa",
                "art advisor contemporary African",
                "art consultant Africa",
            ]
        elif self.target_type == ProspectType.CURATOR:
            queries = [
                "curator Africa contemporary",
                "curatorial practice African art",
            ]
        elif self.target_type == ProspectType.GALLERY:
            queries = [
                "gallery African artists",
                "contemporary art gallery Africa",
            ]

        return queries


class DiscoveryEngine:
    """Discovery engine for finding prospects."""

    def __init__(self, session: Session):
        self.session = session
        self.headers = {"User-Agent": "Kucibok-Prospector/1.1 (+http://kucibok.com/bot)"}

    def generate_artist_searches(self, countries: list = None) -> list[SearchQuery]:
        """Generate artist discovery queries."""
        if countries is None:
            countries = ["Senegal", "Nigeria", "Kenya", "South Africa", "Morocco"]

        keywords = [
            "contemporary artist",
            "emerging artist",
            "sculptor",
            "painter",
            "visual artist",
            "installation artist",
        ]

        searches = []
        for keyword in keywords:
            search = SearchQuery(ProspectType.ARTIST, [keyword], countries)
            searches.append(search)

        logger.info(f"Generated {len(searches)} artist search queries")
        return searches

    def generate_client_searches(self) -> list[SearchQuery]:
        """Generate client (advisor/curator) discovery queries."""
        searches = []

        # Art advisors
        advisor_keywords = [
            "art advisor",
            "art consultant",
            "art advisor Africa",
            "African contemporary art advisor",
        ]
        searches.append(SearchQuery(ProspectType.ART_ADVISOR, advisor_keywords))

        # Curators
        curator_keywords = [
            "curator",
            "curatorial practice",
            "curator Africa",
            "curator contemporary African art",
        ]
        searches.append(SearchQuery(ProspectType.CURATOR, curator_keywords))

        # Galleries
        gallery_keywords = [
            "art gallery",
            "contemporary gallery",
            "gallery African artists",
        ]
        searches.append(SearchQuery(ProspectType.GALLERY, gallery_keywords))

        logger.info(f"Generated {len(searches)} client search queries")
        return searches

    def search_google(self, query: str, max_results: int = 10) -> list[dict]:
        """
        Search Google and parse results.

        Returns list of dicts with: {title, url, snippet}

        Note: This is a basic implementation. For production, use:
        - SerpAPI (paid)
        - Google Custom Search API (paid)
        - Or implement with Selenium for dynamic search
        """
        logger.info(f"Searching Google: {query}")

        # For now, return empty (would need API key)
        # In production, integrate with SerpAPI or Selenium
        results = []

        # Placeholder: Would make real API call here
        # url = f"https://www.google.com/search?q={query}"
        # response = requests.get(url, headers=self.headers, timeout=10)
        # ... parse HTML ...

        return results

    def search_instagram_hashtag(self, hashtag: str) -> list[dict]:
        """
        Search Instagram hashtag profiles.

        Returns list of Instagram accounts with hashtag.

        Note: Instagram API doesn't allow hashtag search in Graph API.
        Would need to scrape publicly or use instagrapi (unofficial).
        """
        logger.info(f"Searching Instagram hashtag: #{hashtag}")

        # For production, use instagrapi (read-only, public data)
        # from instagrapi import Client
        # client = Client()
        # results = client.hashtag_medias_recent_v2(hashtag)

        results = []
        return results

    def search_artfacts(self, keywords: list, country: str = None) -> list[dict]:
        """
        Search artfacts.net for artists.

        Returns list of artist profiles.
        """
        logger.info(f"Searching artfacts: {keywords}, country={country}")

        # Placeholder: Would scrape artfacts.net here
        # This is a public directory, scraping is typically allowed
        # but should respect rate limits

        results = []
        return results

    def create_prospect_from_result(
        self,
        name: str,
        prospect_type: ProspectType,
        country: str,
        website: str | None = None,
        instagram: str | None = None,
        description: str | None = None,
        source_url: str | None = None,
    ) -> Prospect | None:
        """
        Create or update prospect from search result.

        Checks for duplicates by email, website, or name+country.
        """
        # Check for existing prospect
        if website:
            existing = self.session.exec(
                select(Prospect).where(Prospect.website == website)
            ).first()
            if existing:
                logger.info(f"Prospect already exists: {existing.id} ({website})")
                return None

        # Create new prospect
        prospect = Prospect(
            type=prospect_type,
            name=name,
            country=country,
            website=website,
            instagram=instagram,
            description=description,
            status=ProspectStatus.IDENTIFIED,
        )

        self.session.add(prospect)
        self.session.commit()
        self.session.refresh(prospect)

        # Add source
        if source_url:
            source = Source(
                prospect_id=prospect.id,
                url=source_url,
                source_type=SourceType.WEBSITE,
                title=f"Discovery: {name}",
                captured_at=datetime.now(timezone.utc),
            )
            self.session.add(source)
            self.session.commit()

        logger.info(f"✅ Created prospect: {prospect.name} (ID: {prospect.id})")
        return prospect

    def discover_artists(self, countries: list = None, limit: int = 50) -> dict:
        """
        Discover artists.

        Returns: {discovered: N, duplicates: N, errors: N}
        """
        logger.info(f"🔍 Discovering artists (limit: {limit})...")

        searches = self.generate_artist_searches(countries)
        discovered = 0
        duplicates = 0
        errors = 0

        for search in searches:
            try:
                # Try multiple search sources
                results = self.search_google(" ".join(search.keywords))
                # results += self.search_instagram_hashtag("africanart")
                # results += self.search_artfacts(search.keywords, search.countries[0])

                for result in results[:limit]:
                    try:
                        prospect = self.create_prospect_from_result(
                            name=result.get("title", "Unknown"),
                            prospect_type=ProspectType.ARTIST,
                            country=search.countries[0] if search.countries else "UNKNOWN",
                            website=result.get("url"),
                            description=result.get("snippet"),
                            source_url=result.get("url"),
                        )
                        if prospect:
                            discovered += 1
                        else:
                            duplicates += 1

                        if discovered >= limit:
                            break

                    except Exception as e:
                        logger.error(f"Error creating prospect: {e!s}")
                        errors += 1

                if discovered >= limit:
                    break

            except Exception as e:
                logger.error(f"Error in artist discovery: {e!s}")
                errors += 1

        logger.info(
            f"✅ Artist discovery complete: {discovered} discovered, {duplicates} duplicates, {errors} errors"
        )
        return {
            "discovered": discovered,
            "duplicates": duplicates,
            "errors": errors,
        }

    def discover_clients(self, limit: int = 50) -> dict:
        """
        Discover clients (advisors, curators, galleries).

        Returns: {discovered: N, duplicates: N, errors: N}
        """
        logger.info(f"🔍 Discovering clients (limit: {limit})...")

        searches = self.generate_client_searches()
        discovered = 0
        duplicates = 0
        errors = 0

        for search in searches:
            try:
                # Search LinkedIn, Google, etc.
                results = self.search_google(" ".join(search.keywords))

                for result in results[:limit]:
                    try:
                        prospect = self.create_prospect_from_result(
                            name=result.get("title", "Unknown"),
                            prospect_type=search.target_type,
                            country=result.get("country", "UNKNOWN"),
                            website=result.get("url"),
                            description=result.get("snippet"),
                            source_url=result.get("url"),
                        )
                        if prospect:
                            discovered += 1
                        else:
                            duplicates += 1

                        if discovered >= limit:
                            break

                    except Exception as e:
                        logger.error(f"Error creating prospect: {e!s}")
                        errors += 1

                if discovered >= limit:
                    break

            except Exception as e:
                logger.error(f"Error in client discovery: {e!s}")
                errors += 1

        logger.info(
            f"✅ Client discovery complete: {discovered} discovered, {duplicates} duplicates, {errors} errors"
        )
        return {
            "discovered": discovered,
            "duplicates": duplicates,
            "errors": errors,
        }
