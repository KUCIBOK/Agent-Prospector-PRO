#!/usr/bin/env python
"""Supprimer tous les prospects"""
import requests
from app.db import SessionLocal
from app.models import Prospect

print("🗑️  SUPPRESSION DE TOUS LES PROSPECTS")
print("=" * 70)

session = SessionLocal()

try:
    # Compter avant
    all_prospects = session.query(Prospect).all()
    count_before = len(all_prospects)
    print(f"\n📊 Avant: {count_before} prospects\n")

    # Supprimer tous
    for prospect in all_prospects:
        session.delete(prospect)
    session.commit()

    # Vérifier après
    count_after = len(session.query(Prospect).all())
    print(f"✅ Après: {count_after} prospects")
    print(f"🗑️  Supprimés: {count_before - count_after}")

finally:
    session.close()

print("\n" + "=" * 70)
print("✅ Base de données nettoyée!")
print("=" * 70)
