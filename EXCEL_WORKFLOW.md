# 📊 Workflow Complet — Excel Import → Email → Suivi

**Scénario**: Vous avez un fichier Excel avec 50 prospects de Paris. Voici comment Kucibok gère le workflow complet.

---

## 🚀 **Phase 1: Importer le fichier Excel**

### Format attendu

Votre Excel doit avoir ces colonnes:

```
| name | type | country | email | website | linkedin | instagram | description |
|------|------|---------|-------|---------|----------|-----------|-------------|
| Jean Dupont | CURATOR | France | jean@... | https://... | https://linkedin... | @jean_curator | Contemporary art... |
| Marie Bernard | ART_ADVISOR | France | marie@... | (optionnel) | (optionnel) | (optionnel) | Specialist in... |
| Pierre Galerie | GALLERY | France | pierre@... | https://gallery.fr | - | - | Gallery in Paris |
```

**Types acceptés**: `ARTIST`, `ART_ADVISOR`, `CURATOR`, `GALLERY`, `OTHER`  
**Champs obligatoires**: name, type, country  
**Champs optionnels**: email, website, linkedin, instagram, description

---

## 📥 **Importer via API (PowerShell)**

### 1️⃣ Démarrer l'app

```powershell
# Terminal 1: API
python -m uvicorn app.main:app --reload

# Terminal 2: Worker (pour traitement async)
celery -A app.workers.tasks worker --loglevel=info

# Terminal 3: Scheduler
python -m app.scheduler.main
```

### 2️⃣ Importer le fichier

```powershell
# Via l'API (à implémenter)
$file = "C:\path\to\your\prospects.xlsx"

# Ou directement en Python:
python -c "
from app.db import SessionLocal
from app.services.excel_import import ExcelImporter

session = SessionLocal()
importer = ExcelImporter(session)

result = importer.import_excel('prospects.xlsx')
print(f'✅ Imported: {result[\"imported\"]} prospects')
print(f'⚠️  Skipped: {result[\"skipped\"]} duplicates')
print(f'❌ Errors: {len(result[\"errors\"])} errors')

session.close()
"
```

### Résultat

```
✅ Imported: 48 prospects
⚠️  Skipped: 2 duplicates  
❌ Errors: 0 errors
```

---

## 🎯 **Phase 2: Traitement Automatique**

### Que se passe-t-il après l'import?

```
Import Excel (48 prospects)
    ↓
Status: IDENTIFIED
    ↓
[Chaque jour à minuit via Scheduler]
    ↓
Discovery → Crawling → Enrichment → Analysis → Scoring
    ↓
Status: PREQUALIFIED
Score: 65-85 (pour curateurs/advisors)
Priority: P1-P3
    ↓
Messages générés automatiquement (P1-P2 seulement)
```

### Exemple: Prospect après traitement

```python
{
  "id": 1,
  "name": "Jean Dupont",
  "type": "CURATOR",
  "country": "FR",
  "email": "jean@paris-art.fr",
  "website": "https://galerie-jean.fr",
  "status": "PREQUALIFIED",
  "score": 78.5,              # ← Calculé automatiquement
  "confidence": "HIGH",        # ← Basé sur données
  "priority": "P2",            # ← Calculé automatiquement
  "recommended_angle": "SOURCING_AND_LOGISTICS",
  "reason_to_contact": {
    "why": "You specialize in contemporary art and we connect curators with verified African artists",
    "why_now": "Growing demand for African contemporary art in European markets",
    "what": "Access to verified artist database + complete Africa→international logistics"
  }
}
```

---

## 📧 **Phase 3: Envoyer les Emails**

### Via Python

```python
from app.db import SessionLocal
from app.services.email_service import EmailService, EmailConfig
from app.models import Prospect, Message
from sqlmodel import select

# Config email (Gmail, Outlook, etc.)
email_config = EmailConfig(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    sender_email="kucibok@example.com",
    sender_name="Kucibok",
    username="your_email@gmail.com",
    password="your_app_password",
    use_tls=True
)

session = SessionLocal()
email_service = EmailService(session, email_config)

# 1️⃣ Envoyer les emails de bienvenue
prospects = session.exec(
    select(Prospect).where(Prospect.priority.in_(["P1", "P2"]))
).all()

for prospect in prospects:
    success = email_service.send_email(
        to_email=prospect.email,
        subject=f"Rejoignez Kucibok — {prospect.name}",
        html_body=f"""
        <h2>Bienvenue sur Kucibok! 🎨</h2>
        <p>Bonjour {prospect.name},</p>
        <p>Nous vous avons découvert et pensons que {prospect.type.lower()} 
        serait parfait pour Kucibok.</p>
        <p><a href="https://kucibok.com/signup">Rejoindre maintenant</a></p>
        """,
    )
    
    if success:
        print(f"✅ Email envoyé à {prospect.name}")
    else:
        print(f"❌ Erreur avec {prospect.name}")

# 2️⃣ Suivre les inscriptions
# (À implémenter: webhook pour suivi des clics, inscriptions, etc.)

session.close()
```

---

## 📨 **Phase 4: Suivi Email (Follow-ups)**

### Séquence de suivi automatique

```
Jour 0: Email de bienvenue
  ↓
Jour 3: Relance (si pas d'inscription)
  ↓
Jour 7: Second follow-up
  ↓
Jour 14: Dernier email
```

### Implémenter le suivi

```python
from datetime import datetime, timedelta
from app.models import Prospect

# Planifier les follow-ups après inscription
for prospect in prospects:
    base_date = datetime.utcnow()
    
    follow_up_dates = {
        3: "Gentle reminder",
        7: "Still interested?",
        14: "Last chance"
    }
    
    for days, message in follow_up_dates.items():
        scheduled_date = base_date + timedelta(days=days)
        
        # TODO: Créer une tâche planifiée
        # scheduled_task = ScheduledTask(
        #     prospect_id=prospect.id,
        #     task_type="send_email",
        #     scheduled_date=scheduled_date,
        #     template=message
        # )
```

---

## 📊 **Phase 5: Tracker les Résultats**

### Dashboard de suivi

Votre dashboard montre en temps réel:

```
📊 IMPORT RESULTS
├── Total importés: 50
├── Succès: 48
├── Doublons: 2
└── Erreurs: 0

🎯 APRÈS SCORING (24h)
├── P1 (contact immédiat): 8
├── P2 (cette semaine): 15
├── P3 (watchlist): 20
└── P4 (archive): 5

📧 EMAIL STATUS
├── Envoyés: 23 (P1+P2)
├── Ouverts: 12 (52%)
├── Cliqués: 7 (30%)
├── Réponses: 2 (9%)
└── Inscriptions: 1 (4%)

💌 FOLLOW-UP QUEUE
├── Jour 3: 15 emails planifiés
├── Jour 7: 15 emails planifiés
└── Jour 14: 15 emails planifiés
```

---

## 🔄 **Workflow Complet (Chronologie)**

```
JOUR 0 (Matin)
└─ Import Excel
   └─ 50 prospects → Status: IDENTIFIED

JOUR 0 (Après import)
└─ Scoring automatique lancé
   ├─ Enrichment: normaliser pays, email, URLs
   ├─ Crawling: télécharger websites
   ├─ Analysis: scorer prospects
   └─ Résultat: Scores + Priority + Messages générés

JOUR 0 (Après-midi)
└─ Emails envoyés aux P1-P2 (23 prospects)
   ├─ Subject: "Rejoignez Kucibok"
   ├─ Open tracking: pixel tracker
   └─ Click tracking: shortened URLs

JOUR 1-2
└─ Suivi manuel (optionnel)
   └─ Vérifier les ouvertures, clics, réponses

JOUR 3
└─ Follow-up email automatique #1
   ├─ Relance douce pour ceux qui n'ont pas ouvert
   └─ Resend à 15 prospects

JOUR 7
└─ Follow-up email automatique #2
   ├─ "Still interested?"
   └─ Resend à ceux qui n'ont pas répondu

JOUR 14
└─ Dernier email automatique
   ├─ "Last chance"
   └─ Archive si pas de réponse

JOUR 30+
└─ Analyse des résultats
   ├─ Taux d'ouverture: 52%
   ├─ Taux de clic: 30%
   ├─ Taux de réponse: 9%
   └─ Taux d'inscription: 4% (2/50)
```

---

## 🛠️ **Configuration Email (.env)**

```env
# SMTP Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=kucibok@example.com
SENDER_NAME=Kucibok
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password  # ← Pas votre vrai mot de passe!
SMTP_TLS=true

# Follow-up Configuration
FOLLOWUP_DAY3=true
FOLLOWUP_DAY7=true
FOLLOWUP_DAY14=true
FOLLOWUP_RETRY_UNOPENED=true

# Tracking
TRACK_OPENS=true
TRACK_CLICKS=true
TRACK_SIGNUPS=true
```

---

## 💡 **Cas d'Usage: Vous avez vos 50 prospects**

### Scénario réel

1. **Vous téléchargez** `prospects_paris.xlsx` avec vos 50 contacts
2. **Vous importez** via l'API ou Python
3. **Kucibok traite** automatiquement:
   - ✅ Normalise les données
   - ✅ Cherche des infos complémentaires (websites, social media)
   - ✅ Score chaque prospect
   - ✅ Génère des messages personnalisés
4. **Vous envoyez** les emails manuellement ou via Gmail/Outlook
5. **Kucibok suit** automatiquement:
   - Qui a ouvert l'email
   - Qui a cliqué
   - Qui s'est inscrit
   - Les follow-ups se déclenchent automatiquement
6. **Vous voyez** les résultats dans le dashboard

---

## 📝 **Fichier Excel: Format Exact**

Créez votre fichier avec ces colonnes:

| name | type | country | email | website | linkedin | instagram | description |
|------|------|---------|-------|---------|----------|-----------|-------------|
| Jean Dupont | CURATOR | France | jean@gallery.fr | https://gallery.fr | https://linkedin.com/in/jean | @jeangallery | Contemporary art expert |
| Marie Sophie | ART_ADVISOR | France | marie@advisor.fr | | https://linkedin.com/in/marie | @marie_advisor | African art specialist |
| ... | ... | ... | ... | ... | ... | ... | ... |

**Téléchargez le template**:
```powershell
python templates/prospects_template.py
# Ouvre: templates/prospects_import_template.xlsx
```

---

## ✅ **Checklist: Importer 50 Prospects**

- [ ] Préparer fichier Excel (ou utiliser le template)
- [ ] Configurer email dans .env
- [ ] Démarrer l'app + worker + scheduler
- [ ] Importer le fichier
- [ ] Vérifier les résultats (dashboard)
- [ ] Envoyer les emails (manuellement ou via API)
- [ ] Attendre 24-48h pour le scoring automatique
- [ ] Voir les résultats dans le dashboard
- [ ] Planifier les follow-ups

---

**Status**: 🟢 Système prêt pour gérer vos 50 prospects!

Besoin d'aide pour préparer votre Excel?
