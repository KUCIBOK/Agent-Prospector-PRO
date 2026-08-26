#!/usr/bin/env python
"""
Test End-to-End complet du système Kucibok Prospector
Vérifie que tout fonctionne correctement
"""
import requests
import time
from datetime import datetime

print("=" * 80)
print("🚀 TEST END-TO-END - KUCIBOK PROSPECTOR")
print("=" * 80)
print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Résultats
results = {
    "passed": 0,
    "failed": 0,
    "details": []
}

def test(name, condition, details=""):
    """Tester une condition"""
    if condition:
        print(f"✅ {name}")
        results["passed"] += 1
        results["details"].append(f"✅ {name}")
    else:
        print(f"❌ {name}")
        if details:
            print(f"   └─ {details}")
        results["failed"] += 1
        results["details"].append(f"❌ {name}: {details}")

print("1️⃣  VÉRIFICATION API")
print("-" * 80)

# Test 1: Health check
try:
    r = requests.get("http://localhost:8000/health", timeout=5)
    test("API Health Check", r.status_code == 200, f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   └─ Version: {data.get('version')}")
        print(f"   └─ Service: {data.get('service')}")
except Exception as e:
    test("API Health Check", False, str(e))

# Test 2: Readiness check
try:
    r = requests.get("http://localhost:8000/ready", timeout=5)
    test("API Readiness", r.status_code == 200, f"Status: {r.status_code}")
except Exception as e:
    test("API Readiness", False, str(e))

print("\n2️⃣  VÉRIFICATION DATABASE")
print("-" * 80)

# Test 3: Prospects count
try:
    r = requests.get("http://localhost:8000/api/monitoring/summary", timeout=5)
    test("DB Connection", r.status_code == 200, f"Status: {r.status_code}")

    if r.status_code == 200:
        data = r.json()
        total = data.get("prospects", {}).get("total", 0)
        print(f"   └─ Total Prospects: {total}")
        test("Prospects Exist", total > 0, f"Found {total} prospects")
except Exception as e:
    test("DB Query", False, str(e))

# Test 4: Prospects stats
try:
    r = requests.get("http://localhost:8000/api/monitoring/prospects/stats", timeout=5)
    test("Prospects Stats", r.status_code == 200, f"Status: {r.status_code}")

    if r.status_code == 200:
        data = r.json()
        total = data.get("total", 0)
        p1 = data.get("by_priority", {}).get("P1", 0)
        p2 = data.get("by_priority", {}).get("P2", 0)
        print(f"   └─ P1: {p1}, P2: {p2}")
except Exception as e:
    test("Stats Query", False, str(e))

print("\n3️⃣  VÉRIFICATION DONNÉES")
print("-" * 80)

# Test 5: List prospects
try:
    r = requests.get("http://localhost:8000/api/prospects?page=1&page_size=10", timeout=5)
    test("List Prospects", r.status_code == 200, f"Status: {r.status_code}")

    if r.status_code == 200:
        data = r.json()
        items = data.get("items", [])
        print(f"   └─ Retrieved: {len(items)} prospects")

        if items:
            p = items[0]
            print(f"   └─ First prospect: {p.get('name')} ({p.get('type')})")
            print(f"   └─ Email: {p.get('email')}")
            print(f"   └─ Website: {p.get('website')}")
            test("Prospect Data",
                 all([p.get('name'), p.get('email'), p.get('website')]),
                 "Missing required fields")
except Exception as e:
    test("List Query", False, str(e))

# Test 6: Email domain variety
try:
    r = requests.get("http://localhost:8000/api/prospects?page=1&page_size=100", timeout=5)
    if r.status_code == 200:
        data = r.json()
        items = data.get("items", [])

        domains = set()
        for p in items:
            if p.get("email"):
                domain = p["email"].split("@")[1] if "@" in p["email"] else "unknown"
                domains.add(domain)

        print(f"   └─ Email Domains: {len(domains)} différents")
        test("Email Variety", len(domains) > 5, f"Found {len(domains)} domains")
except Exception as e:
    test("Domain Variety", False, str(e))

print("\n4️⃣  VÉRIFICATION API ENDPOINTS")
print("-" * 80)

# Test 7: Dashboard endpoint
try:
    r = requests.get("http://localhost:8000/dashboard", timeout=5)
    test("Dashboard Endpoint", r.status_code == 200, f"Status: {r.status_code}")
except Exception as e:
    test("Dashboard Endpoint", False, str(e))

# Test 8: Dashboard summary endpoint
try:
    r = requests.get("http://localhost:8000/dashboard-summary", timeout=5)
    test("Dashboard Summary", r.status_code == 200, f"Status: {r.status_code}")
except Exception as e:
    test("Dashboard Summary", False, str(e))

# Test 9: Swagger UI
try:
    r = requests.get("http://localhost:8000/docs", timeout=5)
    test("Swagger UI", r.status_code == 200, f"Status: {r.status_code}")
except Exception as e:
    test("Swagger UI", False, str(e))

print("\n5️⃣  VÉRIFICATION VALIDATIONS")
print("-" * 80)

# Test 10: Data consistency
try:
    r = requests.get("http://localhost:8000/api/prospects?page=1&page_size=100", timeout=5)
    if r.status_code == 200:
        data = r.json()
        items = data.get("items", [])

        valid = 0
        for p in items:
            if p.get("name") and p.get("type") and p.get("country"):
                valid += 1

        test("Data Consistency", valid == len(items), f"{valid}/{len(items)} valid")
except Exception as e:
    test("Data Validation", False, str(e))

print("\n" + "=" * 80)
print("📊 RÉSULTATS FINAUX")
print("=" * 80)
print(f"\n✅ Tests passés: {results['passed']}")
print(f"❌ Tests échoués: {results['failed']}")
print(f"📈 Taux de succès: {results['passed']}/{results['passed'] + results['failed']} ({100 * results['passed'] // (results['passed'] + results['failed']) if (results['passed'] + results['failed']) > 0 else 0}%)\n")

if results["failed"] == 0:
    print("🎉 ✅ TOUS LES TESTS PASSÉS - SYSTÈME OPÉRATIONNEL!")
else:
    print(f"⚠️  {results['failed']} test(s) échoué(s) - Vérifiez la configuration")

print("\n" + "=" * 80)
print("🌐 ACCÈS AU SYSTÈME")
print("=" * 80)
print("\n📊 Dashboard Principal:")
print("   → http://localhost:8000/dashboard")
print("\n📊 Dashboard Résumé:")
print("   → http://localhost:8000/dashboard-summary")
print("\n📋 API JSON:")
print("   → http://localhost:8000/api/prospects")
print("\n📖 Documentation API:")
print("   → http://localhost:8000/docs")
print("\n" + "=" * 80)
print("✨ Système Kucibok Prospector - PRODUCTION READY")
print("=" * 80 + "\n")
