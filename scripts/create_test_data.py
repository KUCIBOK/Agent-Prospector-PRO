#!/usr/bin/env python3
"""Create sample test data for Kucibok Prospector."""

from sqlmodel import Session
from app.models import (
    Prospect,
    ProspectType,
    ProspectStatus,
)

# Test artists data
TEST_ARTISTS = [
    {
        "name": "Aïssatou Sarr",
        "country": "SN",
        "city": "Dakar",
        "website": "https://aissatousarr.com",
        "instagram": "@aissatousarr",
        "specialty": "Textile & Installation Art",
        "description": "Contemporary African artist focusing on sustainable textiles",
    },
    {
        "name": "Oshogbo Contemporary",
        "country": "NG",
        "city": "Lagos",
        "website": "https://oshogbo.gallery",
        "instagram": "@oshogbo_gallery",
        "specialty": "Contemporary Sculpture",
        "description": "Gallery showcasing emerging Nigerian sculptors",
    },
]

# Test advisors/curators data
TEST_CURATORS = [
    {
        "name": "Michel Adanson Galleries",
        "country": "FR",
        "city": "Paris",
        "website": "https://adanson-galleries.fr",
        "specialty": "African Contemporary Art",
        "description": "Parisian gallery specialized in African contemporary art",
    },
]


def create_test_data():
    """Create sample test data in the database."""
    from app.db import engine

    with Session(engine) as session:
        print("Creating test data...")
        print()

        # Create test artists
        print("Creating test artists...")
        for artist_data in TEST_ARTISTS:
            prospect = Prospect(
                type=ProspectType.ARTIST,
                name=artist_data["name"],
                country=artist_data["country"],
                city=artist_data.get("city"),
                website=artist_data.get("website"),
                instagram=artist_data.get("instagram"),
                specialty=artist_data.get("specialty"),
                description=artist_data.get("description"),
                status=ProspectStatus.IDENTIFIED,
                score=75.0,
                confidence="MEDIUM",
            )
            session.add(prospect)
            print(f"  - {prospect.name} ({prospect.country})")

        session.commit()
        print()

        # Create test curators
        print("Creating test curators/advisors...")
        for curator_data in TEST_CURATORS:
            prospect = Prospect(
                type=ProspectType.CURATOR,
                name=curator_data["name"],
                country=curator_data["country"],
                city=curator_data.get("city"),
                website=curator_data.get("website"),
                specialty=curator_data.get("specialty"),
                description=curator_data.get("description"),
                status=ProspectStatus.IDENTIFIED,
                score=80.0,
                confidence="HIGH",
            )
            session.add(prospect)
            print(f"  - {prospect.name} ({prospect.country})")

        session.commit()
        print()
        print("Test data created successfully!")


if __name__ == "__main__":
    create_test_data()
