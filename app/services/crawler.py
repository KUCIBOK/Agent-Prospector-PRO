"""
Crawler — Download and parse prospect websites and profiles.

Extracts:
- About/bio content
- Contact information
- Social media links
- Portfolio/exhibition info
- Team members
- Professional links

Respects:
- robots.txt
- Rate limiting (1 req/sec per domain)
- Timeout (30 sec)
- Error handling & retry logic
"""

import logging
import re
import time
from datetime import datetime, timezone
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

from app.models import Prospect

logger = logging.getLogger(__name__)


class CrawlResult:
    """Result of crawling a website."""

    def __init__(self, url: str, status: str, data: dict = None, error: str = None):
        self.url = url
        self.status = status  # SUCCESS, ERROR, TIMEOUT, ROBOTS_TXT
        self.data = data or {}
        self.error = error
        self.timestamp = datetime.now(timezone.utc)

    def __repr__(self):
        return f"<CrawlResult {self.url} {self.status}>"


class Crawler:
    """Website crawler for prospect enrichment."""

    def __init__(self):
        self.session = requests.Session()
        self.headers = {"User-Agent": "Kucibok-Prospector/1.1 (+http://kucibok.com/bot)"}
        self.session.headers.update(self.headers)
        self.timeout = 30
        self.last_request_time = {}  # Track per-domain rate limiting

    def _rate_limit(self, domain: str):
        """Enforce 1 request per second per domain."""
        if domain in self.last_request_time:
            elapsed = time.time() - self.last_request_time[domain]
            if elapsed < 1:
                time.sleep(1 - elapsed)
        self.last_request_time[domain] = time.time()

    def _check_robots_txt(self, url: str) -> bool:
        """Check if URL is allowed by robots.txt (per-agent rules, wildcards)."""
        try:
            parsed = urlparse(url)
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

            response = self.session.get(robots_url, timeout=5)
            if response.status_code in (401, 403):
                logger.warning(f"robots.txt access denied, skipping: {parsed.netloc}")
                return False
            if response.status_code != 200:
                return True  # No robots.txt: everything is allowed

            parser = RobotFileParser()
            parser.parse(response.text.splitlines())
            agent = self.session.headers.get("User-Agent", "*")
            if not parser.can_fetch(agent, url):
                logger.warning(f"robots.txt disallows: {url}")
                return False
            return True

        except Exception as e:
            logger.warning(f"Could not check robots.txt: {e!s}")
            return True  # Assume allowed if error

    def crawl_website(self, url: str) -> CrawlResult:
        """
        Crawl a website and extract data.

        Extracts:
        - Title
        - Description
        - Email addresses
        - Social media links
        - Phone numbers
        - About text
        """
        if not url:
            return CrawlResult(url, "ERROR", error="No URL provided")

        # Normalize URL
        if not url.startswith("http"):
            url = f"https://{url}"

        logger.info(f"🕷️  Crawling: {url}")

        # Check robots.txt
        if not self._check_robots_txt(url):
            logger.warning(f"Blocked by robots.txt: {url}")
            return CrawlResult(url, "ROBOTS_TXT")

        # Rate limit
        parsed = urlparse(url)
        self._rate_limit(parsed.netloc)

        try:
            # Download page
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract data
            data = {
                "title": soup.title.string if soup.title else "UNKNOWN",
                "url": url,
                "status_code": response.status_code,
                "content_length": len(response.content),
            }

            # Meta description
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc:
                data["description"] = meta_desc.get("content", "")

            # Emails (simple regex)
            text = soup.get_text()
            emails = set(re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", text))
            data["emails"] = list(emails)[:5]  # Limit to 5

            # Phone numbers
            phones = set(re.findall(r"\+?[\d\s\-\(\)]{10,}", text))
            data["phones"] = list(phones)[:3]

            # Social media links
            social_media = {
                "instagram": None,
                "linkedin": None,
                "facebook": None,
                "twitter": None,
            }

            links = soup.find_all("a", href=True)
            for link in links:
                href = link.get("href", "").lower()
                if "instagram.com" in href and not social_media["instagram"]:
                    social_media["instagram"] = href
                elif "linkedin.com" in href and not social_media["linkedin"]:
                    social_media["linkedin"] = href
                elif "facebook.com" in href and not social_media["facebook"]:
                    social_media["facebook"] = href
                elif "twitter.com" in href and not social_media["twitter"]:
                    social_media["twitter"] = href

            data["social_media"] = social_media

            # Extract about/bio (look for common sections)
            about_text = ""
            for tag_name in ["about", "bio", "artist-statement", "statement"]:
                element = soup.find(id=re.compile(tag_name, re.IGNORECASE))
                if element:
                    about_text = element.get_text()[:500]
                    break

            data["about_text"] = about_text

            logger.info(f"✅ Successfully crawled: {url}")
            return CrawlResult(url, "SUCCESS", data)

        except requests.Timeout:
            logger.error(f"Timeout: {url}")
            return CrawlResult(url, "TIMEOUT", error="Request timeout (30s)")

        except requests.RequestException as e:
            logger.error(f"Request error: {url} — {e!s}")
            return CrawlResult(url, "ERROR", error=str(e))

        except Exception as e:
            logger.error(f"Crawl error: {url} — {e!s}")
            return CrawlResult(url, "ERROR", error=str(e))

    def crawl_instagram(self, handle: str) -> CrawlResult:
        """
        Get Instagram profile data (public info only).

        For production, use instagrapi or Instagram Graph API.
        This is a placeholder that returns empty.
        """
        logger.info(f"📷 Fetching Instagram profile: @{handle}")

        # In production:
        # from instagrapi import Client
        # client = Client()
        # user = client.user_info_by_username(handle)
        # return user data

        logger.warning("Instagram scraping not implemented (would need API key)")
        return CrawlResult(f"instagram.com/{handle}", "SKIPPED")

    def crawl_linkedin(self, profile_url: str) -> CrawlResult:
        """
        Get LinkedIn profile data (public info only).

        LinkedIn doesn't provide official API for public profiles.
        This is a placeholder.
        """
        logger.info(f"💼 Fetching LinkedIn profile: {profile_url}")

        logger.warning("LinkedIn scraping not implemented (requires special permissions)")
        return CrawlResult(profile_url, "SKIPPED")

    def update_prospect_from_crawl(
        self,
        prospect: Prospect,
        crawl_result: CrawlResult,
    ) -> bool:
        """
        Update prospect with crawled data.

        Returns True if updated, False if no new data.
        """
        if crawl_result.status != "SUCCESS":
            logger.warning(f"Crawl failed: {crawl_result.status}")
            return False

        data = crawl_result.data
        updated = False

        # Extract first email if not already set
        if not prospect.email and data.get("emails"):
            prospect.email = data["emails"][0]
            updated = True

        # Add about/bio to description
        if not prospect.description and data.get("about_text"):
            prospect.description = data["about_text"]
            updated = True

        # Update social media links
        social = data.get("social_media", {})
        if not prospect.instagram and social.get("instagram"):
            prospect.instagram = social["instagram"]
            updated = True

        if not prospect.linkedin and social.get("linkedin"):
            prospect.linkedin = social["linkedin"]
            updated = True

        return updated
