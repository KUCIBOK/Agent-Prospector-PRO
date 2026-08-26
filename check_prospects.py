#!/usr/bin/env python
"""
Vérifier les prospects actuels dans la base de données
"""
import requests

print("📊 VÉRIFICATION DES PROSPECTS À PARIS")
print("=" * 70)

try:
    # Récupérer les stats
    response = requests.get('http://localhost:8000/api/monitoring/summary')
    data = response.json()

    print("\n📊 STATISTIQUES GLOBALES:")
    print("-" * 70)
    print(f"Total Prospects: {data['prospects']['total']}")
    print(f"  ├─ Artistes: {data['prospects']['artists']}")
    print(f"  └─ Clients (Curators/Galleries): {data['prospects']['clients']}")

    print(f"\n✉️  MESSAGES:")
    print(f"  ├─ Total: {data['messages']['total']}")
    print(f"  ├─ Brouillon: {data['messages']['draft']}")
    print(f"  ├─ Envoyés: {data['messages']['sent']}")
    print(f"  └─ Répondus: {data['messages']['draft']}")

    print(f"\n🔔 SIGNAUX RÉCENTS (7 jours): {data['signals']['recent']}")
    print(f"⏱️  Uptime: {data['uptime_seconds']} secondes")

    # Récupérer les prospects
    print("\n" + "=" * 70)
    print("🎯 TOP 10 DERNIERS PROSPECTS:")
    print("=" * 70)

    resp2 = requests.get('http://localhost:8000/api/prospects?page=1&page_size=10&sort=-created_at')
    prospects_data = resp2.json()

    if prospects_data['items'] and len(prospects_data['items']) > 0:
        for i, p in enumerate(prospects_data['items'], 1):
            print(f"\n{i}. {p.get('name', 'N/A')}")
            print(f"   Type: {p.get('type', '?')}")
            if p.get('email'):
                print(f"   📧  {p['email']}")
            if p.get('website'):
                print(f"   🌐  {p['website']}")
            if p.get('country'):
                print(f"   📍  {p['country']}")
            if p.get('priority'):
                print(f"   ⚡  Priority: {p['priority']}")
            if p.get('description'):
                print(f"   📝  {p['description'][:100]}...")
    else:
        print("\n❌ Aucun prospect trouvé dans la base de données")

    # Statistiques par type
    print("\n" + "=" * 70)
    print("📈 PROSPECTS PAR PRIORITÉ:")
    print("=" * 70)

    stats_resp = requests.get('http://localhost:8000/api/monitoring/prospects/stats')
    stats = stats_resp.json()

    if 'by_priority' in stats:
        for priority, count in stats['by_priority'].items():
            if count > 0:
                print(f"   {priority}: {count} prospects")

    print("\n" + "=" * 70)
    print("✅ Vérification complétée!")
    print("=" * 70)

except requests.exceptions.ConnectionError:
    print("\n❌ Impossible de se connecter à l'API")
    print("   Vérifiez que l'API est lancée sur http://localhost:8000")
except Exception as e:
    print(f"\n❌ Erreur: {str(e)}")
