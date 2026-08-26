#!/usr/bin/env python
"""
Script de sourcing: Lancer Deep Source pour 100 prospects à Paris
"""
import time
import requests
import sys

def main():
    print("🚀 KUCIBOK PROSPECTOR - SOURCING 100 PROSPECTS À PARIS")
    print("=" * 60)

    # Attendre que l'API démarre
    print("\n⏳ Attente du démarrage de l'API...")
    max_retries = 20
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print("✅ API ACTIVE! Prêt pour le sourcing.\n")
                break
        except:
            sys.stdout.write(f"\r⏳ Tentative {i+1}/{max_retries}...")
            sys.stdout.flush()
            time.sleep(1)

    # Lancer Deep Source
    print("🔥 Lancement du sourcing: 100 prospects...\n")
    print("   • Recherche sur Google")
    print("   • Extraction des emails/websites")
    print("   • Création des prospects")
    print("   • Status: IDENTIFIED\n")

    try:
        print("📡 Envoi de la requête...")
        response = requests.post(
            "http://localhost:8000/api/prospects/deep-source?target_count=100",
            timeout=180
        )

        if response.status_code == 200:
            data = response.json()
            print("\n" + "=" * 60)
            print("✅ SOURCING COMPLÉTÉ!")
            print("=" * 60)
            print(f"\n📊 RÉSULTATS:")
            print(f"   ✅ Created: {data.get('created', 0)} prospects")
            print(f"   ⚠️  Duplicates: {data.get('duplicates', 0)} removed")
            print(f"   ❌ Errors: {data.get('errors', 0)}")
            print(f"   📍 Location: Paris (détectée automatiquement)")

            print(f"\n📋 Message: {data.get('message', '')}")

            if data.get('prospects'):
                print(f"\n🎯 Aperçu des {min(5, len(data['prospects']))} premiers prospects:")
                for i, prospect in enumerate(data['prospects'][:5], 1):
                    print(f"\n   {i}. {prospect.get('name', 'N/A')}")
                    if prospect.get('email'):
                        print(f"      📧 {prospect['email']}")
                    if prospect.get('website'):
                        print(f"      🌐 {prospect['website']}")
                    if prospect.get('country'):
                        print(f"      📍 {prospect['country']}")

            print("\n" + "=" * 60)
            print("🎉 Prospects prêts pour:")
            print("   ✅ Enrichissement (websites, emails)")
            print("   ✅ Scoring (SaaS Fit, Priority)")
            print("   ✅ Outreach (Sourcing & Vetting emails)")
            print("   ✅ Follow-ups (Auto-send j3, j7, j14)")
            print("=" * 60)

        else:
            print(f"\n❌ Erreur HTTP {response.status_code}")
            print(f"   Response: {response.text}")

    except requests.exceptions.Timeout:
        print("\n❌ Timeout - Le sourcing prend trop de temps")
        print("   L'API est peut-être surchargée")
    except requests.exceptions.ConnectionError:
        print("\n❌ Impossible de se connecter à l'API")
        print("   Vérifiez que l'API est lancée: python -m uvicorn app.main:app --port 8000")
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")

if __name__ == "__main__":
    main()
