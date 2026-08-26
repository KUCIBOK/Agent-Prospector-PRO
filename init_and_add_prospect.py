#!/usr/bin/env python
"""
Initialiser la base de données et ajouter le prospect thugmoc@gmail.com
"""
from datetime import datetime, timezone
from sqlmodel import SQLModel, create_engine, Session
import sys
import os

# Ajouter le répertoire au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importer les modèles
from app.models.prospect import Prospect, ProspectType, ProspectStatus, Priority, ConfidenceLevel

print("🚀 INITIALISATION BASE DE DONNÉES + AJOUT PROSPECT\n")

# Créer ou connecter à la base de données
DATABASE_URL = "sqlite:///prospects.db"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

print("1️⃣  Création des tables...")
try:
    SQLModel.metadata.create_all(engine)
    print("✅ Tables créées avec succès\n")
except Exception as e:
    print(f"⚠️  Tables existantes (OK): {e}\n")

# Créer et ajouter le prospect
print("2️⃣  Ajout du prospect thugmoc@gmail.com...")

prospect = Prospect(
    type=ProspectType.CURATOR,
    name="Thug Moc",
    country="FR",
    city="Paris",
    website="https://www.thugmoc-art.fr",
    email="thugmoc@gmail.com",
    description="Professional curator and art specialist",
    specialty="Contemporary African Art",
    africa_interest="HIGH",
    international_activity="HIGH",
    digital_maturity="HIGH",
    status=ProspectStatus.IDENTIFIED,
    score=80.0,
    confidence=ConfidenceLevel.HIGH,
    priority=Priority.P1,
    recommended_angle="DISCOVERY",
    reason_to_contact="Curator specializing in contemporary art - excellent fit for partnership",
    last_verified_at=datetime.now(timezone.utc)
)

try:
    with Session(engine) as session:
        # Vérifier si le prospect existe déjà
        existing = session.query(Prospect).filter(
            Prospect.email == "thugmoc@gmail.com"
        ).first()

        if existing:
            print(f"✅ Prospect '{prospect.name}' ({prospect.email}) existe déjà (ID: {existing.id})")
        else:
            # Ajouter le nouveau prospect
            session.add(prospect)
            session.commit()
            session.refresh(prospect)
            print(f"✅ Prospect ajouté avec succès!")
            print(f"   └─ ID: {prospect.id}")
            print(f"   └─ Name: {prospect.name}")
            print(f"   └─ Email: {prospect.email}")
            print(f"   └─ Priority: {prospect.priority}")
            print(f"   └─ Score: {prospect.score}")

except Exception as e:
    print(f"❌ Erreur lors de l'ajout: {str(e)}")
    import traceback
    traceback.print_exc()

# Vérifier le total des prospects
print("\n3️⃣  Vérification finale...")
try:
    with Session(engine) as session:
        total = session.query(Prospect).count()
        p1_count = session.query(Prospect).filter(Prospect.priority == Priority.P1).count()
        print(f"✅ Total prospects dans la base: {total}")
        print(f"   └─ P1 (HOT): {p1_count}")
except Exception as e:
    print(f"⚠️  Erreur lors de la vérification: {e}")

print("\n" + "="*80)
print("✅ INITIALISATION COMPLÈTE")
print("="*80 + "\n")
