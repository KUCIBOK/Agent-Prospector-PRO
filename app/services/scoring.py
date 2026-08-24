"""
Scoring service — calculate fit scores for prospects.

Based on LOGIC.md:
- Artist Fit Score (/100)
- SaaS Fit Score (/100)
- Confidence Score (LOW/MEDIUM/HIGH)
- Priority Score (P1–P4)
"""

from typing import Optional
from app.models import Prospect, Priority, ConfidenceLevel


def calculate_artist_fit_score(prospect: Prospect) -> tuple[float, dict]:
    """
    Calculate Artist Fit Score (/100).

    Components:
    - Profile Quality (20)
    - International Potential (20)
    - Digital Presence (15)
    - Commercial Potential (20)
    - Work Documentation (15)
    - Kucibok Fit (10)

    Returns:
        (score, breakdown)
    """
    score = 0
    breakdown = {}

    # 1. Profile Quality (20 points)
    profile_quality = 0
    if prospect.description and len(prospect.description) > 50:
        profile_quality += 10
    if prospect.city:
        profile_quality += 5
    if prospect.specialty:
        profile_quality += 5
    score += profile_quality
    breakdown["profile_quality"] = min(profile_quality, 20)

    # 2. International Potential (20 points)
    intl_potential = 0
    if prospect.website:
        intl_potential += 10
    if prospect.africa_interest and prospect.africa_interest.upper() != "UNKNOWN":
        intl_potential += 10
    score += intl_potential
    breakdown["international_potential"] = min(intl_potential, 20)

    # 3. Digital Presence (15 points)
    digital_presence = 0
    if prospect.website:
        digital_presence += 5
    if prospect.instagram:
        digital_presence += 5
    if prospect.linkedin:
        digital_presence += 5
    score += digital_presence
    breakdown["digital_presence"] = min(digital_presence, 15)

    # 4. Commercial Potential (20 points)
    commercial = 0
    if prospect.instagram:
        commercial += 10
    if prospect.website:
        commercial += 10
    score += commercial
    breakdown["commercial_potential"] = min(commercial, 20)

    # 5. Work Documentation (15 points)
    # TODO: Check from sources/portfolio
    documentation = 5  # Base score
    breakdown["work_documentation"] = documentation

    # 6. Kucibok Fit (10 points)
    # TODO: Based on previous interactions
    fit = 5  # Base score
    breakdown["kucibok_fit"] = fit

    return min(score, 100), breakdown


def calculate_saas_fit_score(prospect: Prospect) -> tuple[float, dict]:
    """
    Calculate SaaS Fit Score (/100) for clients.

    Components:
    - African Sourcing Need (30)
    - Operational Need (20)
    - International Activity (15)
    - Commercial Capacity (15)
    - Digital Maturity (10)
    - Intent Signal (10)

    Returns:
        (score, breakdown)
    """
    score = 0
    breakdown = {}

    # 1. African Sourcing Need (30 points)
    # TODO: Based on past activity, interests
    sourcing = 0
    if prospect.africa_interest:
        if prospect.africa_interest.upper() == "HIGH":
            sourcing = 30
        elif prospect.africa_interest.upper() == "MEDIUM":
            sourcing = 15
        else:
            sourcing = 5
    score += sourcing
    breakdown["african_sourcing_need"] = sourcing

    # 2. Operational Need (20 points)
    # TODO: Based on international activity
    operational = 0
    if prospect.international_activity:
        if prospect.international_activity.upper() == "HIGH":
            operational = 20
        elif prospect.international_activity.upper() == "MEDIUM":
            operational = 10
    score += operational
    breakdown["operational_need"] = operational

    # 3. International Activity (15 points)
    intl = 0
    if prospect.website:
        intl += 5
    if prospect.linkedin:
        intl += 10
    score += intl
    breakdown["international_activity"] = min(intl, 15)

    # 4. Commercial Capacity (15 points)
    # TODO: Based on business type, size
    commercial = 5  # Base
    breakdown["commercial_capacity"] = commercial

    # 5. Digital Maturity (10 points)
    digital = 0
    if prospect.digital_maturity:
        if prospect.digital_maturity.upper() == "HIGH":
            digital = 10
        elif prospect.digital_maturity.upper() == "MEDIUM":
            digital = 5
    score += digital
    breakdown["digital_maturity"] = digital

    # 6. Intent Signal (10 points)
    # TODO: Based on detected signals
    intent = 0
    breakdown["intent_signal"] = intent

    return min(score, 100), breakdown


def calculate_confidence_score(prospect: Prospect) -> ConfidenceLevel:
    """
    Calculate Confidence Score based on data completeness.

    Returns:
        LOW / MEDIUM / HIGH
    """
    data_points = 0
    total_possible = 8

    if prospect.email:
        data_points += 1
    if prospect.website:
        data_points += 1
    if prospect.linkedin:
        data_points += 1
    if prospect.instagram:
        data_points += 1
    if prospect.description:
        data_points += 1
    if prospect.specialty:
        data_points += 1
    if prospect.city:
        data_points += 1
    if prospect.digital_maturity:
        data_points += 1

    ratio = data_points / total_possible
    if ratio >= 0.75:
        return ConfidenceLevel.HIGH
    elif ratio >= 0.5:
        return ConfidenceLevel.MEDIUM
    else:
        return ConfidenceLevel.LOW


def calculate_priority(
    fit_score: float,
    confidence: ConfidenceLevel,
) -> Priority:
    """
    Calculate Priority (P1–P4) based on fit score and confidence.

    P1: Contact immediately (fit > 80 + HIGH confidence)
    P2: Contact this week (fit > 65 + MEDIUM confidence)
    P3: Nurturing / watchlist (fit > 50 OR new)
    P4: Archive
    """
    if fit_score >= 80 and confidence == ConfidenceLevel.HIGH:
        return Priority.P1
    elif fit_score >= 65 and confidence in [ConfidenceLevel.MEDIUM, ConfidenceLevel.HIGH]:
        return Priority.P2
    elif fit_score >= 50:
        return Priority.P3
    else:
        return Priority.P4


def is_contact_ready(prospect: Prospect) -> bool:
    """
    Check if prospect meets minimum quality threshold for outreach.

    Rules (QUALITY GATE #3):
    - (Score >= 75 AND Confidence = HIGH) OR
    - (Score >= 85 AND Confidence = MEDIUM)
    - Must have email AND LinkedIn confirmed

    Lower quality prospects → P3/P4 for nurturing, NOT P1/P2 outreach.

    Returns:
        True if ready to contact, False if should nurture instead
    """
    # Must-have: confirmed contact channels
    if not prospect.email or not prospect.linkedin:
        return False

    # Rule 1: High confidence threshold is lower (75+)
    if prospect.score >= 75 and prospect.confidence == ConfidenceLevel.HIGH:
        return True

    # Rule 2: Medium confidence requires higher score (85+)
    if prospect.score >= 85 and prospect.confidence == ConfidenceLevel.MEDIUM:
        return True

    # Everything else: P3/P4 nurturing only, never P1/P2
    return False
