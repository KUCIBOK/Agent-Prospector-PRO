"""
AI Analysis Service — Use LLM for prospect analysis.

Analyzes:
- Africa interest level
- International activity
- Digital maturity
- Intent signals
- Reason to contact
- Recommended angle
"""

import json
import logging
from typing import Optional

from sqlmodel import Session

from app.models import Prospect, AIAnalysis
from app.ai.providers import AIProvider

logger = logging.getLogger(__name__)


class AnalysisService:
    """Prospect analysis service using AI."""

    def __init__(self, session: Session, ai_provider: AIProvider):
        self.session = session
        self.ai = ai_provider

    def analyze_africa_interest(self, prospect: Prospect) -> str:
        """
        Determine Africa interest level: HIGH / MEDIUM / LOW / UNKNOWN
        """
        if prospect.africa_interest and prospect.africa_interest.upper() in ["HIGH", "MEDIUM", "LOW"]:
            return prospect.africa_interest

        # Check description, specialty for clues
        text = (prospect.description or "") + " " + (prospect.specialty or "")
        text_lower = text.lower()

        if any(
            word in text_lower
            for word in ["africa", "african", "senegal", "nigeria", "kenya", "south africa"]
        ):
            if any(word in text_lower for word in ["specializes", "focused", "expertise"]):
                return "HIGH"
            return "MEDIUM"

        return "UNKNOWN"

    def analyze_international_activity(self, prospect: Prospect) -> str:
        """
        Determine international activity level: HIGH / MEDIUM / LOW / UNKNOWN
        """
        if prospect.international_activity and prospect.international_activity.upper() in ["HIGH", "MEDIUM", "LOW"]:
            return prospect.international_activity

        # Check for international indicators
        text = (prospect.description or "") + " " + (prospect.specialty or "")
        text_lower = text.lower()

        score = 0
        if prospect.website and prospect.website.startswith("http"):
            score += 2
        if prospect.linkedin:
            score += 1
        if prospect.instagram:
            score += 1
        if any(word in text_lower for word in ["international", "global", "export", "worldwide"]):
            score += 2

        if score >= 4:
            return "HIGH"
        elif score >= 2:
            return "MEDIUM"

        return "UNKNOWN"

    def analyze_digital_maturity(self, prospect: Prospect) -> str:
        """
        Determine digital maturity: HIGH / MEDIUM / LOW / UNKNOWN
        """
        if prospect.digital_maturity and prospect.digital_maturity.upper() in ["HIGH", "MEDIUM", "LOW"]:
            return prospect.digital_maturity

        # Count digital touchpoints
        score = 0
        if prospect.website:
            score += 3
        if prospect.instagram:
            score += 2
        if prospect.linkedin:
            score += 2
        if prospect.email:
            score += 1

        if score >= 5:
            return "HIGH"
        elif score >= 2:
            return "MEDIUM"

        return "LOW"

    def analyze_prospect(self, prospect: Prospect) -> dict:
        """
        Comprehensive AI-powered prospect analysis.

        Returns:
        {
            "africa_interest": "HIGH/MEDIUM/LOW/UNKNOWN",
            "international_activity": "HIGH/MEDIUM/LOW/UNKNOWN",
            "digital_maturity": "HIGH/MEDIUM/LOW/UNKNOWN",
            "reason_to_contact": {
                "why": "...",
                "why_now": "...",
                "what": "..."
            },
            "recommended_angle": "SOURCING/LOGISTICS/...",
            "signals": [...]
        }
        """
        logger.info(f"🧠 Analyzing prospect: {prospect.name} (ID: {prospect.id})")

        analysis = {
            "africa_interest": self.analyze_africa_interest(prospect),
            "international_activity": self.analyze_international_activity(prospect),
            "digital_maturity": self.analyze_digital_maturity(prospect),
        }

        # Generate reason to contact (rule-based)
        analysis["reason_to_contact"] = self._generate_reason_to_contact(prospect, analysis)

        # Recommended angle (rule-based)
        analysis["recommended_angle"] = self._recommend_angle(prospect, analysis)

        # Store analysis
        ai_analysis = AIAnalysis(
            prospect_id=prospect.id,
            analysis_type="comprehensive",
            raw_output=analysis,
            model_version="1.0",
        )
        self.session.add(ai_analysis)
        self.session.commit()

        logger.info(f"✅ Analysis complete for {prospect.name}")
        return analysis

    def _generate_reason_to_contact(self, prospect: Prospect, analysis: dict) -> dict:
        """
        Generate reason to contact (rule-based, no LLM).

        Guardrail: Only use data explicitly in prospect record.
        """
        why = ""
        why_now = ""
        what = ""

        # WHY
        if analysis["africa_interest"] in ["HIGH", "MEDIUM"]:
            why = f"You specialize in African art and we connect curators with verified African artists."
        elif prospect.type.value == "GALLERY":
            why = "You're a gallery that could benefit from sourcing African artists."
        elif prospect.type.value == "ART_ADVISOR":
            why = "As an art advisor, you likely work with collectors interested in contemporary art."
        else:
            why = f"Your background in {prospect.specialty or 'art'} aligns with our network."

        # WHY NOW
        if analysis["international_activity"] in ["HIGH", "MEDIUM"]:
            why_now = "We help international art professionals access African artists efficiently."
        else:
            why_now = "There's a growing demand for African contemporary art in international markets."

        # WHAT
        if prospect.type.value == "CURATOR":
            what = "We offer a verified artist database + complete Africa→international logistics."
        elif prospect.type.value == "ART_ADVISOR":
            what = "Direct access to emerging African artists and end-to-end project management."
        elif prospect.type.value == "GALLERY":
            what = "Sourcing partnerships with African artists and simplified customs handling."
        else:
            what = "A platform to source, vet, and manage relationships with African artists."

        return {
            "why": why,
            "why_now": why_now,
            "what": what,
        }

    def _recommend_angle(self, prospect: Prospect, analysis: dict) -> str:
        """
        Recommend outreach angle (rule-based).

        SOURCING: Help finding artists
        LOGISTICS: Help with customs, shipping
        SOURCING_AND_LOGISTICS: Both
        DISCOVERY: General discovery
        INTERNATIONAL_ACCESS: Access to new market
        """
        # Check history - do they already work with African artists?
        text = (prospect.description or "") + " " + (prospect.specialty or "")
        text_lower = text.lower()

        if any(word in text_lower for word in ["african", "senegal", "nigeria", "kenya"]):
            if any(word in text_lower for word in ["logistics", "shipping", "customs", "export"]):
                return "LOGISTICS"
            elif any(word in text_lower for word in ["new", "expand", "discover", "looking"]):
                return "SOURCING_AND_LOGISTICS"
            else:
                return "SOURCING"

        # For those with no African experience
        if analysis["international_activity"] == "HIGH":
            return "INTERNATIONAL_ACCESS"

        if prospect.type.value in ["CURATOR", "ART_ADVISOR"]:
            return "SOURCING_AND_LOGISTICS"

        return "SOURCING"

    def batch_analyze_prospects(self, limit: int = 50) -> dict:
        """
        Analyze multiple prospects.

        Returns: {analyzed: N, total: N}
        """
        from app.models import ProspectStatus
        from sqlmodel import select

        logger.info(f"🧠 Batch analyzing prospects (limit: {limit})...")

        # Get prospects needing analysis
        prospects = self.session.exec(
            select(Prospect)
            .where(Prospect.status == ProspectStatus.IDENTIFIED)
            .order_by(Prospect.created_at.desc())
            .limit(limit)
        ).all()

        analyzed = 0
        for prospect in prospects:
            try:
                # Only analyze if not already analyzed
                from sqlmodel import select
                existing = self.session.exec(
                    select(AIAnalysis)
                    .where(AIAnalysis.prospect_id == prospect.id)
                    .where(AIAnalysis.analysis_type == "comprehensive")
                ).first()

                if not existing:
                    analysis = self.analyze_prospect(prospect)
                    analyzed += 1

            except Exception as e:
                logger.error(f"Error analyzing {prospect.name}: {str(e)}")

        logger.info(f"✅ Batch analysis complete: {analyzed}/{len(prospects)} prospects analyzed")
        return {
            "analyzed": analyzed,
            "total": len(prospects),
        }
