#!/usr/bin/env python
"""
Recréer les 75 prospects réalistes avec domaines emails variés
"""
from datetime import datetime, timezone
from sqlmodel import SQLModel, create_engine, Session, select
import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models.prospect import Prospect, ProspectType, ProspectStatus, Priority, ConfidenceLevel

print("🚀 RECRÉATION DES 75 PROSPECTS RÉALISTES\n")

# Base de données
DATABASE_URL = "sqlite:///prospects.db"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

# 18 domaines emails variés (artistes/curators parisiens)
EMAIL_DOMAINS = [
    "artgallery.fr",
    "curator.paris",
    "galerieparis.fr",
    "contemporaryart.paris",
    "arte.fr",
    "galerie-contemporaine.fr",
    "artcurator.fr",
    "parisiangallery.fr",
    "galeriemoderne.fr",
    "artcenter.fr",
    "galerieart.paris",
    "artisans.fr",
    "curatorial.paris",
    "artadvice.fr",
    "galleryspace.paris",
    "modernart.fr",
    "artspecialist.paris",
    "gmail.com",
    "hotmail.fr"
]

# Noms français
FIRST_NAMES = [
    "Jean", "Marie", "Pierre", "Anne", "Michel", "Sophie", "Philippe", "Nicole",
    "Claude", "Isabelle", "François", "Martine", "Laurent", "Véronique", "André",
    "Chantal", "Bernard", "Dominique", "Alain", "Sylvie", "Christian", "Monique",
    "Georges", "Brigitte", "Yves", "Florence", "Henri", "Delphine", "Roger",
    "Nathalie", "Marcel", "Roseline", "Marc", "Stéphanie", "Paul", "Valérie"
]

LAST_NAMES = [
    "Moreau", "Dubois", "Durand", "Petit", "Dumont", "Fontaine", "Vincennes",
    "Leclerc", "Lefebvre", "Martin", "Rousseau", "Blanc", "Morel", "Michel",
    "Garcia", "Rossi", "Gérard", "Fabre", "Leconte", "Lemaire"
]

CITIES = ["Paris", "Versailles", "Neuilly", "Saint-Honoré", "Marais", "Bastille",
          "Belleville", "Montmartre", "Champs-Élysées", "Left Bank"]

SPECIALTIES = [
    "Contemporary African Art",
    "Modern Art",
    "Emerging Artists",
    "Abstract Art",
    "Figurative Art",
    "Digital Art",
    "Sculpture",
    "Photography",
    "Mixed Media",
    "Installation Art"
]

print("1️⃣  Génération des prospects...\n")

# Fixer seed pour reproductibilité
random.seed(42)

prospects_to_add = []

# Créer 75 prospects
for i in range(75):
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    name = f"{first_name} {last_name}"

    email_local = f"{first_name.lower()}.{last_name.lower()}".replace(" ", "")
    email_domain = random.choice(EMAIL_DOMAINS)
    email = f"{email_local}@{email_domain}"

    city = random.choice(CITIES)
    # Rendre le website unique avec un numéro
    website = f"https://www.{first_name.lower()}-{last_name.lower()}-{i:03d}.fr"
    specialty = random.choice(SPECIALTIES)

    # Scores aléatoires
    fair_score = random.randint(60, 95)
    gallery_score = random.randint(65, 90)
    awards_score = random.randint(40, 85)
    final_score = round((fair_score * 0.35) + (gallery_score * 0.35) + (awards_score * 0.30), 1)

    # Déterminer la priorité
    if final_score >= 75:
        priority = Priority.P1
        confidence = ConfidenceLevel.HIGH
    elif final_score >= 60:
        priority = Priority.P2
        confidence = ConfidenceLevel.MEDIUM
    else:
        priority = Priority.P3
        confidence = ConfidenceLevel.LOW

    prospect = Prospect(
        type=ProspectType.CURATOR,
        name=name,
        country="FR",
        city=city,
        website=website,
        email=email,
        description=f"Professional {specialty.lower()} curator in Paris",
        specialty=specialty,
        africa_interest="HIGH",
        international_activity="HIGH",
        digital_maturity="MEDIUM",
        status=ProspectStatus.IDENTIFIED,
        score=final_score,
        confidence=confidence,
        priority=priority,
        recommended_angle="DISCOVERY",
        reason_to_contact=f"Expert in {specialty} - strong fit for partnership",
        last_verified_at=datetime.now(timezone.utc)
    )

    prospects_to_add.append(prospect)

    if (i + 1) % 10 == 0:
        print(f"   ✓ {i + 1} prospects générés")

print(f"\n✅ {len(prospects_to_add)} prospects générés\n")

# Ajouter à la base de données
print("2️⃣  Ajout à la base de données...\n")

added_count = 0
skipped_count = 0

try:
    with Session(engine) as session:
        for prospect in prospects_to_add:
            # Vérifier si le prospect existe déjà
            statement = select(Prospect).where(Prospect.email == prospect.email)
            existing = session.exec(statement).first()

            if existing:
                skipped_count += 1
            else:
                session.add(prospect)
                added_count += 1

        session.commit()
        print(f"✅ {added_count} nouveaux prospects ajoutés")
        print(f"⏭️  {skipped_count} prospects existants (non dupliqués)\n")

except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

# Vérifier les statistiques finales
print("3️⃣  Vérification finale...\n")

try:
    with Session(engine) as session:
        statement = select(Prospect)
        all_prospects = session.exec(statement).all()

        total = len(all_prospects)
        p1_count = len([p for p in all_prospects if p.priority == Priority.P1])
        p2_count = len([p for p in all_prospects if p.priority == Priority.P2])
        p3_count = len([p for p in all_prospects if p.priority == Priority.P3])

        # Domaines emails utilisés
        domains = set()
        for p in all_prospects:
            if p.email and "@" in p.email:
                domain = p.email.split("@")[1]
                domains.add(domain)

        print(f"📊 STATISTIQUES FINALES:")
        print(f"   Total prospects: {total}")
        print(f"   └─ P1 (HOT): {p1_count}")
        print(f"   └─ P2 (Nurture): {p2_count}")
        print(f"   └─ P3 (Watchlist): {p3_count}")
        print(f"\n📧 Email domains utilisés: {len(domains)}")
        for domain in sorted(domains):
            print(f"   • {domain}")

except Exception as e:
    print(f"⚠️  Erreur lors de la vérification: {e}")

print("\n" + "="*80)
print(f"✅ SYSTÈME PRÊT - {total} PROSPECTS EN BASE")
print("="*80 + "\n")
