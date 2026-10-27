"""
Intent Signals Detection — identify recent activities indicating buying/hiring intent.

Detects:
1. LinkedIn title/role changes (director → founder, added new curators)
2. Recent Africa exhibitions (new shows, residencies)
3. New job postings for "African Art Curator", "Art Advisor"
4. Gallery/institution rebranding or expansion
5. Recent gallery openings or relocations
"""

import logging
from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from app.db import SessionLocal
from app.models import Prospect, Signal

logger = logging.getLogger(__name__)


class IntentSignalDetector:
    """Detect intent signals for existing prospects."""

    def __init__(self, session: Session):
        self.session = session

    def detect_all_signals(self) -> int:
        """
        Scan all prospects for recent intent signals.

        Returns count of new signals detected.
        """
        prospects = self.session.exec(select(Prospect)).all()
        signal_count = 0

        logger.info(f"🔍 Scanning {len(prospects)} prospects for intent signals...")

        for prospect in prospects:
            signals = self.detect_prospect_signals(prospect)
            signal_count += len(signals)

            # If signals found → upgrade priority
            if signals:
                self._upgrade_priority(prospect)

        logger.info(f"✅ Intent detection complete: {signal_count} signals detected")
        return signal_count

    def detect_prospect_signals(self, prospect: Prospect) -> list[Signal]:
        """
        Detect signals for a single prospect.

        Returns list of new signals.
        """
        signals: list[Signal] = []

        # 1. LinkedIn changes (title, new recruits, endorsements)
        linkedin_signals = self._check_linkedin_changes(prospect)
        signals.extend(linkedin_signals)

        # 2. Recent exhibitions with Africa theme
        expo_signals = self._check_africa_exhibitions(prospect)
        signals.extend(expo_signals)

        # 3. Hiring signals (curator/advisor roles)
        hiring_signals = self._check_hiring_signals(prospect)
        signals.extend(hiring_signals)

        # 4. Gallery expansion/relocation
        expansion_signals = self._check_gallery_expansion(prospect)
        signals.extend(expansion_signals)

        # Save new signals to DB
        for signal in signals:
            self.session.add(signal)

        if signals:
            self.session.commit()

        return signals

    def _check_linkedin_changes(self, prospect: Prospect) -> list[Signal]:
        """
        Check for LinkedIn profile changes (title, role, endorsements).

        In production: scrape/monitor LinkedIn profile updates.
        For now: placeholder for integration with LinkedIn API or webhooks.
        """
        signals: list[Signal] = []

        if not prospect.linkedin:
            return signals

        # TODO: Integrate with LinkedIn API (Proxycurl, RocketReach, etc.)
        # For now, this is the framework:
        """
        profile_data = fetch_linkedin_profile(prospect.linkedin)

        # Check title change
        if profile_data['title'] != prospect.cached_linkedin_title:
            signal = Signal(
                prospect_id=prospect.id,
                signal_type=SignalType.CAREER_CHANGE,
                description=f"Title changed to: {profile_data['title']}",
                source_url=prospect.linkedin,
                signal_date=datetime.now(timezone.utc),
                importance=Importance.HIGH,
                confidence=Confidence.HIGH
            )
            signals.append(signal)

        # Check new recruits in company
        if len(profile_data['recent_company_hires']) > 5:
            signal = Signal(
                prospect_id=prospect.id,
                signal_type=SignalType.HIRING_SPREE,
                description=f"{len(profile_data['recent_company_hires'])} new hires in {profile_data['company']} recently",
                source_url=prospect.linkedin,
                signal_date=datetime.now(timezone.utc),
                importance=Importance.MEDIUM,
                confidence=Confidence.MEDIUM
            )
            signals.append(signal)
        """

        return signals

    def _check_africa_exhibitions(self, prospect: Prospect) -> list[Signal]:
        """
        Check for recent exhibitions with Africa theme.

        In production: scrape Artfacts, Artnet, gallery websites, press releases.
        """
        signals: list[Signal] = []

        # TODO: Integrate with exhibition APIs or scraping
        # Placeholder framework:
        """
        exhibitions = search_exhibitions(
            query=f"{prospect.name} OR {prospect.country}",
            theme_filter="Africa",
            date_range_days=30
        )

        for expo in exhibitions:
            if "Africa" in expo['theme'] or "African" in expo['theme']:
                signal = Signal(
                    prospect_id=prospect.id,
                    signal_type=SignalType.AFRICA_EXHIBITION,
                    description=f"Upcoming exhibition: {expo['title']} ({expo['venue']})",
                    source_url=expo['url'],
                    signal_date=datetime.now(timezone.utc),
                    importance=Importance.HIGH,
                    confidence=Confidence.HIGH
                )
                signals.append(signal)
        """

        return signals

    def _check_hiring_signals(self, prospect: Prospect) -> list[Signal]:
        """
        Check for job postings for curator/advisor roles in prospect's org.

        In production: scrape LinkedIn Jobs, Indeed, Artsy Jobs, Idealist.org
        """
        signals: list[Signal] = []

        # TODO: Integrate with job posting APIs
        """
        jobs = search_jobs(
            company=prospect.name or prospect.linked_company,
            keywords=["curator", "art advisor", "artist liaison"],
            date_range_days=30
        )

        if jobs:
            for job in jobs:
                signal = Signal(
                    prospect_id=prospect.id,
                    signal_type=SignalType.HIRING_CURATOR,
                    description=f"Open position: {job['title']}",
                    source_url=job['url'],
                    signal_date=datetime.now(timezone.utc),
                    importance=Importance.HIGH,
                    confidence=Confidence.HIGH
                )
                signals.append(signal)
        """

        return signals

    def _check_gallery_expansion(self, prospect: Prospect) -> list[Signal]:
        """
        Check for gallery expansion, relocation, or new artist representation.

        In production: scrape Artnet, Artfacts, gallery websites, press releases.
        """
        signals: list[Signal] = []

        # TODO: Integrate with gallery database and press monitoring
        """
        gallery_news = search_gallery_news(
            gallery_name=prospect.name,
            date_range_days=30
        )

        for news in gallery_news:
            if any(keyword in news['title'].lower()
                   for keyword in ['expansion', 'opening', 'relocation', 'new location',
                                 'new artists', 'representation', 'Africa']):
                signal = Signal(
                    prospect_id=prospect.id,
                    signal_type=SignalType.GALLERY_EXPANSION,
                    description=news['title'],
                    source_url=news['url'],
                    signal_date=datetime.now(timezone.utc),
                    importance=Importance.MEDIUM,
                    confidence=Confidence.MEDIUM
                )
                signals.append(signal)
        """

        return signals

    def _upgrade_priority(self, prospect: Prospect) -> None:
        """
        Upgrade prospect priority if recent signals detected.

        Rule: Signal found in last 7 days → bump up by 1 level
        """
        from app.models import Priority

        cutoff = datetime.now(timezone.utc) - timedelta(days=7)
        recent_signals = self.session.exec(
            select(Signal).where(
                (Signal.prospect_id == prospect.id) & (Signal.signal_date >= cutoff)
            )
        ).all()

        if not recent_signals:
            return

        # Upgrade logic
        priority_upgrade_map = {
            Priority.P4: Priority.P3,
            Priority.P3: Priority.P2,
            Priority.P2: Priority.P1,
            Priority.P1: Priority.P1,  # Already top
        }

        if prospect.priority:
            new_priority = priority_upgrade_map.get(prospect.priority, prospect.priority)
            if new_priority != prospect.priority:
                logger.info(
                    f"⬆️  Upgrading {prospect.name} from {prospect.priority} → {new_priority} "
                    f"(found {len(recent_signals)} signals)"
                )
                prospect.priority = new_priority
                self.session.add(prospect)
                self.session.commit()


def detect_intent_signals_sync() -> int:
    """Helper for manual trigger or testing."""
    session = SessionLocal()
    try:
        detector = IntentSignalDetector(session)
        return detector.detect_all_signals()
    finally:
        session.close()
