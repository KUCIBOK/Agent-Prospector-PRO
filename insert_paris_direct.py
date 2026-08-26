#!/usr/bin/env python
"""
Insérer 100 prospects directement dans la base de données
Contourne l'API (ne pas passer par FastAPI)
"""
import sys
import uuid
from datetime import datetime

# Importer directement de l'app
from app.db import SessionLocal
from app.models import Prospect, ProspectType

def generate_prospect(index):
    """Générer un prospect unique"""
    first_names = ["Marie", "Jean", "Sophie", "Pierre", "Anne", "Michel", "Claire", "Luc",
                   "Isabelle", "Philippe", "Catherine", "Jacques", "Nicole", "Laurent"]
    last_names = ["Dubois", "Martin", "Bernard", "Fontaine", "Lefevre", "Roux", "Blanc", "Moreau"]

    first_name = first_names[index % len(first_names)]
    last_name = last_names[(index * 7) % len(last_names)]

    # Email et website UNIQUES
    uuid_suffix = str(uuid.uuid4())[:6]
    email = f"curator_{index}_{uuid_suffix}@galerie-paris.fr"
    website = f"https://galerie-{index}-{uuid_suffix}.paris.fr"

    return Prospect(
        type=ProspectType.CURATOR if index % 2 == 0 else ProspectType.GALLERY,
        name=f"{first_name} {last_name} #{index}",
        country="FR",
        city="Paris",
        email=email,
        website=website,
        description=f"Professional curator specializing in contemporary art",
        priority="P1" if index % 5 == 0 else ("P2" if index % 3 == 0 else "P3"),
        status="IDENTIFIED",
    )

def main():
    print("🚀 INSERTION DIRECTE - 100 PROSPECTS À PARIS")
    print("=" * 70)
    print("\n📊 Insertion directe dans la base de données...\n")

    session = SessionLocal()
    created = 0
    errors = 0

    try:
        for i in range(100):
            if i % 10 == 0 and i > 0:
                print(f"   [{i}/100] {created} insérés | {errors} erreurs")

            try:
                prospect = generate_prospect(i)
                session.add(prospect)
                session.commit()
                created += 1

            except Exception as e:
                session.rollback()
                errors += 1
                if errors <= 3:
                    print(f"   ⚠️  Erreur {i}: {str(e)[:60]}...")

    finally:
        session.close()

    print("\n" + "=" * 70)
    print("✅ INSERTION COMPLÉTÉE!")
    print("=" * 70)
    print(f"\n📊 RÉSULTATS:")
    print(f"   ✅ Insérés: {created} prospects")
    print(f"   ❌ Erreurs: {errors}")
    print(f"   📍 Location: Paris, France")
    print(f"   🎯 Types: Curators & Galleries")
    print(f"   ⚡ Priorities: P1, P2, P3")

    print(f"\n" + "=" * 70)
    print("🎉 Prospects prêts!")
    print("=" * 70)

    print(f"\n📊 Vérifier dans le dashboard:")
    print(f"   http://localhost:8000/dashboard.html")

if __name__ == "__main__":
    main()
