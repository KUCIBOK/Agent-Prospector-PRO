"""
Enrichment Service — Fill missing data, normalize fields.

Normalizations:
- Country: ISO 3166-1 codes via pycountry
- Email: lowercase, remove whitespace
- URL: standardize (https, trailing slash)
- Name: title case, strip whitespace
- Phone: remove non-digits

Detects:
- Intent signals from description/data
- Professional indicators
"""

import logging
import re
from typing import Optional
from datetime import datetime

import pycountry
from sqlmodel import Session

from app.models import Prospect, Signal, SignalType, Importance, Confidence

logger = logging.getLogger(__name__)


class Enrichment:
    """Data enrichment service."""

    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def normalize_country(country: str) -> Optional[str]:
        """
        Normalize country name to ISO 3166-1 alpha-2 code.

        Examples:
        - "Senegal" → "SN"
        - "South Africa" → "ZA"
        - "sn" → "SN"
        - "UNKNOWN" → None
        """
        if not country or country.upper() == "UNKNOWN":
            return None

        # Try direct lookup (might be code already)
        try:
            country_obj = pycountry.countries.get(alpha_2=country.upper())
            if country_obj:
                return country_obj.alpha_2
        except:
            pass

        # Try by name
        try:
            country_obj = pycountry.countries.search_fuzzy(country.strip())
            if country_obj:
                return country_obj[0].alpha_2
        except:
            pass

        logger.warning(f"Could not normalize country: {country}")
        return None

    @staticmethod
    def normalize_email(email: Optional[str]) -> Optional[str]:
        """
        Normalize email address.

        Returns lowercase, strips whitespace. None if invalid.
        """
        if not email:
            return None

        email = email.strip().lower()

        # Basic validation
        if "@" not in email or "." not in email:
            return None

        # Remove common invalid patterns
        if email.startswith(".") or email.endswith("."):
            return None

        return email

    @staticmethod
    def normalize_url(url: Optional[str]) -> Optional[str]:
        """
        Normalize URL.

        Adds https://, removes trailing slash.
        """
        if not url:
            return None

        url = url.strip()

        if not url.startswith("http"):
            url = f"https://{url}"

        # Remove trailing slash
        if url.endswith("/"):
            url = url[:-1]

        return url

    @staticmethod
    def normalize_name(name: Optional[str]) -> Optional[str]:
        """
        Normalize name.

        Strips whitespace, title case.
        """
        if not name:
            return None

        name = name.strip()

        # Simple title case (doesn't handle all edge cases)
        name = " ".join(word.capitalize() for word in name.split())

        return name

    @staticmethod
    def normalize_phone(phone: Optional[str]) -> Optional[str]:
        """
        Normalize phone number.

        Keeps only digits and '+'. Returns None if invalid.
        """
        if not phone:
            return None

        # Keep only digits and +
        phone = re.sub(r"[^\d+]", "", phone)

        # Check if it looks like a phone number (at least 10 digits)
        digits = re.sub(r"\D", "", phone)
        if len(digits) < 10:
            return None

        return phone

    def enrich_prospect(self, prospect: Prospect, crawl_data: dict = None) -> Prospect:
        """
        Enrich prospect data with normalizations.

        Args:
            prospect: Prospect to enrich
            crawl_data: Optional data from crawler

        Returns:
            Updated prospect
        """
        logger.info(f"🔄 Enriching prospect: {prospect.name} (ID: {prospect.id})")

        updated = False

        # Normalize country
        if prospect.country:
            normalized_country = self.normalize_country(prospect.country)
            if normalized_country and prospect.country != normalized_country:
                prospect.country = normalized_country
                updated = True

        # Normalize email
        if prospect.email:
            normalized_email = self.normalize_email(prospect.email)
            if normalized_email and prospect.email != normalized_email:
                prospect.email = normalized_email
                updated = True

        # Normalize website
        if prospect.website:
            normalized_website = self.normalize_url(prospect.website)
            if normalized_website and prospect.website != normalized_website:
                prospect.website = normalized_website
                updated = True

        # Normalize name
        if prospect.name:
            normalized_name = self.normalize_name(prospect.name)
            if normalized_name and prospect.name != normalized_name:
                prospect.name = normalized_name
                updated = True

        # Add data from crawl if provided
        if crawl_data:
            if not prospect.email and crawl_data.get("emails"):
                prospect.email = self.normalize_email(crawl_data["emails"][0])
                updated = True

            if not prospect.description and crawl_data.get("description"):
                prospect.description = crawl_data["description"]
                updated = True

            if not prospect.instagram and crawl_data.get("social_media", {}).get("instagram"):
                prospect.instagram = crawl_data["social_media"]["instagram"]
                updated = True

            if not prospect.linkedin and crawl_data.get("social_media", {}).get("linkedin"):
                prospect.linkedin = crawl_data["social_media"]["linkedin"]
                updated = True

        if updated:
            prospect.updated_at = datetime.utcnow()
            self.session.add(prospect)
            self.session.commit()
            logger.info(f"✅ Enriched prospect: {prospect.name}")

        return prospect

    def detect_intent_signals(self, prospect: Prospect) -> list[Signal]:
        """
        Detect intent signals from prospect data.

        Looks for keywords indicating:
        - New exhibition
        - Call for artists
        - Fair participation
        - Program launch
        - International activity
        - Recent publication
        - Partnership
        - Acquisition
        """
        signals = []
        text = (
            (prospect.description or "") + " "
            + (prospect.specialty or "") + " "
            + (prospect.africa_interest or "")
        ).lower()

        if not text.strip():
            return signals

        # Exhibition signals
        if any(word in text for word in ["exhibition", "expo", "show", "displayed"]):
            signal = Signal(
                prospect_id=prospect.id,
                signal_type=SignalType.NEW_EXHIBITION,
                description="Detected exhibition activity",
                signal_date=datetime.utcnow(),
                importance=Importance.MEDIUM,
                confidence=Confidence.MEDIUM,
            )
            signals.append(signal)

        # Call for artists
        if any(
            word in text
            for word in ["call for artists", "open call", "submissions", "apply now"]
        ):
            signal = Signal(
                prospect_id=prospect.id,
                signal_type=SignalType.CALL_FOR_ARTISTS,
                description="Detected call for artists",
                signal_date=datetime.utcnow(),
                importance=Importance.HIGH,
                confidence=Confidence.MEDIUM,
            )
            signals.append(signal)

        # Fair participation
        if any(word in text for word in ["fair", "biennial", "triennial", "biennale"]):
            signal = Signal(
                prospect_id=prospect.id,
                signal_type=SignalType.FAIR_PARTICIPATION,
                description="Detected fair/biennial participation",
                signal_date=datetime.utcnow(),
                importance=Importance.MEDIUM,
                confidence=Confidence.MEDIUM,
            )
            signals.append(signal)

        # International activity
        if any(
            word in text
            for word in [
                "international",
                "global",
                "export",
                "import",
                "worldwide",
            ]
        ):
            signal = Signal(
                prospect_id=prospect.id,
                signal_type=SignalType.INTERNATIONAL_ACTIVITY,
                description="Detected international activity",
                signal_date=datetime.utcnow(),
                importance=Importance.MEDIUM,
                confidence=Confidence.MEDIUM,
            )
            signals.append(signal)

        # Africa interest (already in data, but flag as signal)
        if prospect.africa_interest and prospect.africa_interest.upper() in ["HIGH", "MEDIUM"]:
            signal = Signal(
                prospect_id=prospect.id,
                signal_type=SignalType.INTERNATIONAL_ACTIVITY,
                description=f"Detected Africa interest: {prospect.africa_interest}",
                signal_date=datetime.utcnow(),
                importance=Importance.HIGH if prospect.africa_interest.upper() == "HIGH" else Importance.MEDIUM,
                confidence=Confidence.HIGH,
            )
            signals.append(signal)

        # Save signals
        for signal in signals:
            self.session.add(signal)

        if signals:
            self.session.commit()
            logger.info(f"✅ Detected {len(signals)} signals for {prospect.name}")

        return signals

    def bulk_enrich_prospects(self, limit: int = 100) -> dict:
        """
        Enrich multiple prospects.

        Returns: {enriched: N, total: N}
        """
        from app.models import ProspectStatus
        from sqlmodel import select

        logger.info(f"🔄 Bulk enrichment (limit: {limit})...")

        # Get prospects needing enrichment
        prospects = self.session.exec(
            select(Prospect)
            .where(Prospect.status == ProspectStatus.IDENTIFIED)
            .limit(limit)
        ).all()

        enriched = 0
        for prospect in prospects:
            try:
                self.enrich_prospect(prospect)
                self.detect_intent_signals(prospect)
                enriched += 1
            except Exception as e:
                logger.error(f"Error enriching {prospect.name}: {str(e)}")

        logger.info(f"✅ Bulk enrichment complete: {enriched}/{len(prospects)} prospects")
        return {
            "enriched": enriched,
            "total": len(prospects),
        }
