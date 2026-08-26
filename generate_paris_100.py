#!/usr/bin/env python
"""
Générateur robuste de 100 prospects à Paris avec emails UNIQUES
"""
import requests
import time
import uuid
from datetime import datetime

def generate_unique_prospect(index):
    """Générer un prospect unique"""

    # Noms de base
    first_names = ["Marie", "Jean", "Sophie", "Pierre", "Anne", "Michel", "Claire", "Luc",
                   "Isabelle", "Philippe", "Catherine", "Jacques", "Nicole", "Laurent",
                   "Héléne", "Dominique", "Valérie", "Christophe", "Monique", "Antoine",
                   "Sylvie", "Robert", "Ludivine", "Olivier", "Pascale", "Bernard",
                   "Marcelle", "Frederic", "Gisèle", "Thierry", "Anne", "Serge"]

    last_names = ["Dubois", "Martin", "Bernard", "Fontaine", "Lefevre", "Roux", "Blanc",
                  "Moreau", "Delorme", "Legrand", "Girard", "Arnould", "Camus", "Maillet",
                  "Coste", "Lavigne", "Gibert", "Motte", "Vincent", "Saunier", "Mercier",
                  "Adam", "Bigot", "Carré", "Delaunay", "Devant"]

    first_name = first_names[index % len(first_names)]
    last_name = last_names[(index * 7) % len(last_names)]

    # Email UNIQUE avec index
    unique_suffix = str(uuid.uuid4())[:8]
    email = f"{first_name.lower()}.{last_name.lower()}{index}_{unique_suffix}@galerie-paris.fr"

    # Website UNIQUE avec index
    website = f"https://www.{first_name.lower()}-{last_name.lower()}-{index}.paris-gallery.fr"

    prospect = {
        "name": f"{first_name} {last_name} #{index}",
        "email": email,
        "website": website,
        "country": "FR",
        "city": "Paris",
        "type": "CURATOR" if index % 2 == 0 else "GALLERY",
        "description": f"Professional curator and exhibition specialist #{index}",
        "priority": "P1" if index % 5 == 0 else ("P2" if index % 3 == 0 else "P3"),
    }

    return prospect

def main():
    print("🚀 GÉNÉRATEUR ROBUSTE - 100 PROSPECTS À PARIS")
    print("=" * 70)
    print("\n📊 Génération de 100 prospects uniques...\n")

    created = 0
    duplicates = 0
    errors = 0
    error_details = []

    for i in range(100):
        prospect = generate_unique_prospect(i)

        # Afficher la progression tous les 10
        if i % 10 == 0 and i > 0:
            print(f"   [{i}/100] {created} créés | {duplicates} doublons | {errors} erreurs")

        try:
            response = requests.post(
                "http://localhost:8000/api/prospects",
                json=prospect,
                timeout=10
            )

            if response.status_code == 201:
                created += 1
            elif response.status_code == 409:
                duplicates += 1
            else:
                errors += 1
                error_details.append({
                    "status": response.status_code,
                    "name": prospect["name"],
                    "email": prospect["email"]
                })

        except requests.exceptions.Timeout:
            errors += 1
            error_details.append({"error": "timeout", "name": prospect["name"]})
        except Exception as e:
            errors += 1
            error_details.append({"error": str(e), "name": prospect["name"]})

        # Rate limiting
        time.sleep(0.1)

    print("\n" + "=" * 70)
    print("✅ CRÉATION COMPLÉTÉE!")
    print("=" * 70)
    print(f"\n📊 RÉSULTATS:")
    print(f"   ✅ Created: {created} prospects")
    print(f"   ⚠️  Duplicates: {duplicates}")
    print(f"   ❌ Errors: {errors}")

    if error_details and errors < 10:
        print(f"\n📝 Détails des erreurs:")
        for err in error_details[:5]:
            if "status" in err:
                print(f"   HTTP {err['status']}: {err['name']}")
            else:
                print(f"   {err.get('error', 'unknown')}: {err['name']}")

    print(f"\n" + "=" * 70)
    print("🎉 Résultats:")
    print(f"   📍 Location: Paris, France")
    print(f"   🎯 Types: Curators & Galleries")
    print(f"   ⚡ Priorities: P1, P2, P3")
    print("=" * 70)

    print(f"\n📊 Vérifier les résultats:")
    print(f"   Dashboard: http://localhost:8000/dashboard.html")
    print(f"   API: http://localhost:8000/api/prospects")

if __name__ == "__main__":
    main()
