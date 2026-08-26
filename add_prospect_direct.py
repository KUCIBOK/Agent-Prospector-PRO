#!/usr/bin/env python
"""
Ajouter thugmoc@gmail.com directement à la base de données
"""
import sqlite3
import uuid
from datetime import datetime, timezone

db_path = "prospects.db"

# Données du nouveau prospect
prospect = {
    "id": str(uuid.uuid4()),
    "name": "Thug Moc",
    "email": "thugmoc@gmail.com",
    "website": "https://www.thugmoc-art.fr",
    "country": "FR",
    "city": "Paris",
    "type": "CURATOR",
    "description": "Professional curator and art specialist",
    "priority": "P1",
    "status": "IDENTIFIED",
    "created_at": datetime.now(timezone.utc).isoformat(),
    "updated_at": datetime.now(timezone.utc).isoformat()
}

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Vérifier si le prospect existe déjà
    cursor.execute("SELECT id FROM prospects WHERE email = ?", (prospect["email"],))
    existing = cursor.fetchone()

    if existing:
        print(f"✅ Prospect '{prospect['name']}' ({prospect['email']}) existe déjà")
    else:
        # Insérer le nouveau prospect
        cursor.execute("""
            INSERT INTO prospects
            (id, name, email, website, country, city, type, description, priority, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prospect["id"],
            prospect["name"],
            prospect["email"],
            prospect["website"],
            prospect["country"],
            prospect["city"],
            prospect["type"],
            prospect["description"],
            prospect["priority"],
            prospect["status"],
            prospect["created_at"],
            prospect["updated_at"]
        ))

        conn.commit()
        print(f"✅ Prospect ajouté: {prospect['name']}")
        print(f"   └─ Email: {prospect['email']}")
        print(f"   └─ ID: {prospect['id']}")
        print(f"   └─ Status: P1 (HOT)")

    conn.close()

except Exception as e:
    print(f"❌ Erreur: {str(e)}")
