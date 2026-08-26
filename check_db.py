import sqlite3
import os

db_path = "prospects.db"

if os.path.exists(db_path):
    print(f"✅ Base de données trouvée: {db_path}\n")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Afficher les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print(f"📊 Tables disponibles:")
        for table in tables:
            print(f"   • {table[0]}")

        # Afficher le schéma de la table prospects si elle existe
        if any('prospects' in str(t) for t in tables):
            print(f"\n📋 Schéma de la table 'prospects':")
            cursor.execute("PRAGMA table_info(prospects);")
            columns = cursor.fetchall()
            for col in columns:
                print(f"   • {col[1]} ({col[2]})")
        else:
            print("\n⚠️  La table 'prospects' n'existe pas")

        conn.close()
    except Exception as e:
        print(f"❌ Erreur: {e}")
else:
    print(f"❌ Base de données introuvable: {db_path}")
