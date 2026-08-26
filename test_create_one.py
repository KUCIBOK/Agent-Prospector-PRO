#!/usr/bin/env python
"""
Tester la création d'un seul prospect pour voir l'erreur exacte
"""
import requests
import json

prospect = {
    "name": "Marie Dubois",
    "email": "marie.dubois@galerie-paris.fr",
    "website": "https://www.galerie-dubois-paris.fr",
    "country": "FR",
    "city": "Paris",
    "type": "CURATOR",
    "description": "Professional gallery curator and exhibition specialist",
    "status": "IDENTIFIED",
    "priority": "P1",
    "confidence": "HIGH"
}

print("📤 Création d'un test prospect...")
print(f"Data: {json.dumps(prospect, indent=2, ensure_ascii=False)}\n")

try:
    response = requests.post(
        "http://localhost:8000/api/prospects",
        json=prospect,
        timeout=10
    )

    print(f"Status: {response.status_code}")
    print(f"Response:\n{response.text}")

    if response.status_code >= 400:
        print("\n❌ Erreur!")
        try:
            error = response.json()
            print(f"Error Detail: {error}")
        except:
            print(f"Raw Response: {response.text}")

except Exception as e:
    print(f"❌ Exception: {str(e)}")
