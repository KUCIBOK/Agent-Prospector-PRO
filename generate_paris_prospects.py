#!/usr/bin/env python
"""
Générateur de prospects de test pour Paris
Crée 100 curateurs/galeries à Paris pour tester le système
"""
import requests
import json
from datetime import datetime, timedelta
import random

# Données de base
PARIS_CURATORS_NAMES = [
    "Marie Dubois", "Jean Pierre Morel", "Sophie Leclerc", "André Martin",
    "Isabelle Rousseau", "Philippe Bernard", "Catherine Lefebvre", "Jacques Deschamps",
    "Nicole Garnier", "Pierre Laurent", "Amélie Fontaine", "Michel Bonnet",
    "Claire Remy", "Laurent Vidal", "Héléne Michaud", "Dominique Fournier",
    "Valérie Petit", "Christophe Durand", "Monique Legrand", "Antoine Girard",
    "Sylvie Marin", "Robert Delorme", "Ludivine Benoit", "Olivier Gautier",
    "Pascale Arnould", "Bernard Lefevre", "Marcelle Camus", "Frederic Maillet",
    "Gisèle Coste", "Thierry Lavigne", "Anne Gibert", "Serge Motte",
    "Claudine Bouc", "Alain Lepont", "Denise Rolland", "Eric Fabre",
    "Fabienne Lecomte", "Guy Rossi", "Estelle Ferrand", "Bruno Chevalier",
    "Gloria Vincent", "Henri Saunier", "Irène Mercier", "Jules Adam",
    "Josée Bigot", "Kevin Martin", "Karine Lefebvre", "Luc Bernard",
    "Laure Carre", "Marcel Fontaine", "Margot Delaunay", "Nicolas Devant"
]

GALLERY_NAMES = [
    "Galerie", "Contemporary Art Gallery", "Studio Gallery", "Art Space",
    "Modern Art", "Exhibition Space", "Art Collective", "Creative Hub"
]

DOMAINS = [
    "fr", "com", "eu", "org", "info", "net"
]

def generate_emails_from_name(name: str) -> list:
    """Generate possible email addresses from a name"""
    parts = name.split()
    first = parts[0] if parts else "user"
    last = parts[-1] if len(parts) > 1 else parts[0]
    domain = random.choice(DOMAINS)

    emails = [
        f"{first.lower()}.{last.lower()}@galerie-paris.{domain}",
        f"{first.lower()}@{last.lower()}-art.{domain}",
        f"curator-{first.lower()}@artgallery.{domain}",
        f"{first[0].lower()}{last.lower()}@paris-gallery.{domain}",
    ]
    return emails

def generate_prospect_data():
    """Generate 100 realistic prospects for Paris"""
    prospects = []

    for i, name in enumerate(PARIS_CURATORS_NAMES, 1):
        emails = generate_emails_from_name(name)
        primary_email = random.choice(emails)

        gallery = random.choice(GALLERY_NAMES)
        prospect = {
            "name": name,
            "email": primary_email,
            "website": f"https://www.galerie-{name.split()[1].lower()}-paris.fr",
            "country": "FR",
            "city": "Paris",
            "type": random.choice(["CURATOR", "GALLERY"]),
            "description": f"Professional {gallery} curator and exhibition specialist in contemporary art",
            "status": "IDENTIFIED",
            "priority": random.choice(["P1", "P1", "P1", "P2", "P2", "P2", "P3"]),
            "confidence": random.choice(["HIGH", "MEDIUM", "MEDIUM"])
        }
        prospects.append(prospect)

    # Add 50 more with different generators
    for i in range(50):
        # Random combination
        first_names = ["Marie", "Jean", "Sophie", "Pierre", "Anne", "Michel", "Claire", "Luc"]
        last_names = ["Dubois", "Martin", "Bernard", "Fontaine", "Lefevre", "Roux", "Blanc", "Moreau"]

        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        emails = generate_emails_from_name(name)
        primary_email = random.choice(emails)

        prospect = {
            "name": name,
            "email": primary_email,
            "website": f"https://www.{name.replace(' ', '-').lower()}-art.fr",
            "country": "FR",
            "city": "Paris",
            "type": random.choice(["CURATOR", "ART_ADVISOR", "GALLERY"]),
            "description": "Independent curator specializing in contemporary and emerging artists",
            "status": "IDENTIFIED",
            "priority": random.choice(["P1", "P2", "P2", "P3", "P4"]),
            "confidence": random.choice(["HIGH", "MEDIUM", "MEDIUM", "LOW"])
        }
        prospects.append(prospect)

    return prospects

def main():
    print("🚀 GÉNÉRATEUR DE PROSPECTS - PARIS")
    print("=" * 70)
    print("\n📊 Génération de 100 prospects à Paris...")

    prospects = generate_prospect_data()

    print(f"✅ {len(prospects)} prospects générés\n")
    print("📡 Envoi à l'API...\n")

    created = 0
    duplicates = 0
    errors = 0

    for i, prospect in enumerate(prospects, 1):
        try:
            # Afficher la progression
            if i % 10 == 0:
                print(f"   [{i}/{len(prospects)}] Traitement en cours...")

            response = requests.post(
                "http://localhost:8000/api/prospects",
                json=prospect,
                timeout=10
            )

            if response.status_code == 201:
                created += 1
            elif response.status_code == 409:
                # Duplicate
                duplicates += 1
            else:
                print(f"   ⚠️  Erreur HTTP {response.status_code} pour {prospect['name']}")
                errors += 1

        except requests.exceptions.Timeout:
            print(f"   ⏱️  Timeout pour {prospect['name']}")
            errors += 1
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Impossible de se connecter pour {prospect['name']}")
            errors += 1
        except Exception as e:
            print(f"   ❌ Erreur pour {prospect['name']}: {str(e)}")
            errors += 1

    print("\n" + "=" * 70)
    print("✅ CRÉATION COMPLÉTÉE!")
    print("=" * 70)
    print(f"\n📊 RÉSULTATS:")
    print(f"   ✅ Created: {created} prospects")
    print(f"   ⚠️  Duplicates: {duplicates} (déjà en base)")
    print(f"   ❌ Errors: {errors}")
    print(f"   📍 Location: Paris, France")

    print(f"\n" + "=" * 70)
    print("🎉 Prospects prêts pour:")
    print("   ✅ Enrichissement (websites, emails)")
    print("   ✅ Scoring (SaaS Fit, Priority)")
    print("   ✅ Outreach (Sourcing & Vetting emails)")
    print("   ✅ Analytics et reporting")
    print("=" * 70)

    print(f"\n📊 Voir les résultats:")
    print(f"   Dashboard: http://localhost:8000/dashboard.html")
    print(f"   API: http://localhost:8000/api/prospects")
    print(f"   API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
