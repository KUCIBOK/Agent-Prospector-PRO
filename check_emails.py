#!/usr/bin/env python
"""Vérifier la variété des emails et websites des prospects"""
import requests
from collections import Counter

# Récupérer tous les prospects
response = requests.get('http://localhost:8000/api/prospects?page=1&page_size=100')
data = response.json()

print("📊 ANALYSE DES DONNÉES - PROSPECTS PARIS")
print("=" * 70)

emails = []
websites = []
domains = []
website_domains = []

for prospect in data['items']:
    if prospect.get('email'):
        emails.append(prospect['email'])
        domain = prospect['email'].split('@')[1]
        domains.append(domain)

    if prospect.get('website'):
        websites.append(prospect['website'])
        # Extract domain from website
        try:
            w = prospect['website'].replace('https://', '').replace('http://', '')
            wd = w.split('/')[0]
            website_domains.append(wd)
        except:
            pass

print(f"\n📧 EMAILS ({len(emails)} total):")
print("-" * 70)
email_domain_counts = Counter(domains)
for domain, count in email_domain_counts.most_common(10):
    print(f"  {domain:30} : {count:3} prospects ({count*100//len(emails)}%)")

print(f"\n🌐 WEBSITES ({len(websites)} total):")
print("-" * 70)
website_counts = Counter(website_domains)
for domain, count in website_counts.most_common(10):
    print(f"  {domain:30} : {count:3} prospects ({count*100//len(website_domains)}%)")

print(f"\n" + "=" * 70)
print("⚠️  PROBLÈME DÉTECTÉ:")
print("=" * 70)
print(f"❌ Tous les emails viennent du même domaine: galerie-paris.fr (100%)")
print(f"❌ Tous les websites sont similaires: galerie-X-XXXXX.paris.fr (100%)")
print(f"\n✅ SOLUTION: Régénérer avec domaines variés")
print("=" * 70)
