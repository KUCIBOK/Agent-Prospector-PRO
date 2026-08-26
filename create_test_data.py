#!/usr/bin/env python
"""Create test data for development."""

from app.db import SessionLocal
from app.models import Prospect, ProspectType, ProspectStatus
from datetime import datetime

session = SessionLocal()

prospects_data = [
    {'name': 'Alice Martin', 'email': 'alice@example.com', 'type': ProspectType.ARTIST, 'country': 'France', 'city': 'Paris'},
    {'name': 'Bob Curator', 'email': 'bob@example.com', 'type': ProspectType.CURATOR, 'country': 'France', 'city': 'Lyon'},
    {'name': 'Charlotte Gallery', 'email': 'charlotte@example.com', 'type': ProspectType.CLIENT, 'country': 'France', 'city': 'Marseille'},
    {'name': 'David Collector', 'email': 'david@example.com', 'type': ProspectType.ARTIST, 'country': 'Belgium', 'city': 'Brussels'},
    {'name': 'Eva Paris', 'email': 'eva@example.com', 'type': ProspectType.CURATOR, 'country': 'France', 'city': 'Paris'},
]

print("[*] Creating test prospects...")

for data in prospects_data:
    prospect = Prospect(
        name=data['name'],
        email=data['email'],
        type=data['type'],
        status=ProspectStatus.IDENTIFIED,
        country=data['country'],
        city=data['city'],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    session.add(prospect)
    print(f"[+] Created: {data['name']}")

session.commit()
session.close()
print(f"[OK] Total created: {len(prospects_data)}")
