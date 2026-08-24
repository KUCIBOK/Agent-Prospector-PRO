# 🚀 DÉMARRER LE SYSTÈME COMPLET

**Guide complet pour lancer Kucibok Prospector avec Deep Source!**

```
30 secondes de setup = système 24/7 autonome!
```

---

## 🎯 Objectif Final

```
Vous lancez le système
  ↓
3 AM chaque nuit: Auto-scrape Google, LinkedIn, Instagram
  ↓
Auto-enrichissez 100+ prospects trouvés
  ↓
Auto-scorez et priorityez
  ↓
Auto-envoyez "Sourcing & Vetting" emails
  ↓
Suivez réponses en temps réel sur dashboard
  ↓
30 jours plus tard: 2-3 deals fermés
```

---

## 📋 Checklist Pré-Démarrage

- [ ] Python 3.11+ installé
- [ ] PostgreSQL en cours d'exécution
- [ ] Redis en cours d'exécution (ou Docker)
- [ ] Node.js 18+ (optionnel, pour dashboard)
- [ ] `.env` configuré (voir `.env.example`)

---

## 🚀 Démarrage (3 Terminaux)

### **Terminal 1: FastAPI Server (8000)**

```powershell
# Depuis la racine du projet
python -m uvicorn app.main:app --reload --port 8000

# Output:
# ✅ Uvicorn running on http://127.0.0.1:8000
# 📖 API docs: http://127.0.0.1:8000/docs
```

### **Terminal 2: Celery Worker (async jobs)**

```powershell
# Dans un nouveau terminal
celery -A app.workers.tasks worker --loglevel=info

# Output:
# ✅ celery@YOUR-MACHINE ready to accept tasks
```

### **Terminal 3: Automation Scheduler (3 AM engine)**

```powershell
# Dans un nouveau terminal
python -m app.scheduler.automated_tasks

# Output:
# ✅ Automation scheduler started!
# 📍 Scheduled: Daily prospecting at 3:00 AM
# 📍 Scheduled: Daily follow-ups at 9:00 AM
# 📍 Scheduled: Daily analytics at 6:00 PM
```

**Vous avez un système 24/7 prêt! ✅**

---

## 🔥 Lancer Deep Source (50 prospects)

### **Méthode 1: Script PowerShell (Recommended)**

```powershell
# Terminal 4
.\test_deep_source_api.ps1

# Résultat:
# ✅ Created: 50 hot prospects
# ⏭️  Duplicates: 2 removed
# ❌ Errors: 0 failed
```

### **Méthode 2: Python Script**

```powershell
# Terminal 4
python deep_source_50_prospects.py

# Résultat:
# 🔥 DEEP SOURCE - 50 HOT CURATOR PROSPECTS FROM GOOGLE 🔥
# ✅ Created: 50 hot prospects
```

### **Méthode 3: curl/Invoke-WebRequest**

```powershell
# Récupérer 50 prospects
$response = Invoke-WebRequest `
  -Uri "http://localhost:8000/api/prospects/deep-source?target_count=50" `
  -Method POST

$json = $response.Content | ConvertFrom-Json
Write-Host "✅ Created: $($json.created) prospects"
```

---

## 📊 Vérifier le Système

### **1. Voir les Prospects Créés**

```powershell
# Terminal à part
$response = Invoke-WebRequest "http://localhost:8000/api/prospects?prospect_type=CURATOR&status=IDENTIFIED"
$data = $response.Content | ConvertFrom-Json
Write-Host "Found $($data.total) CURATOR prospects"
```

### **2. Vérifier l'API Docs**

Ouvrez dans le navigateur: **http://localhost:8000/docs**

Vous verrez tous les endpoints:
- `GET /api/prospects` — List prospects
- `POST /api/prospects/deep-source` — Deep source curators
- `GET /api/messages` — View outreach messages
- `GET /api/monitoring/dashboard` — Real-time dashboard

### **3. Voir les Logs**

```powershell
# Terminal 1 (API) — voir les requêtes
# Terminal 2 (Worker) — voir les jobs
# Terminal 3 (Scheduler) — voir les automations
```

---

## 🎯 Workflow Complet

```
JOUR 1 — 10:00 AM
└─ Vous lancez deep_source_50_prospects.py
   └─ 50 curators trouvés + importés ✅

JOUR 1 — 14:00 (14h)
└─ System enrichit automatiquement
   ├─ Scrape websites
   ├─ Extrait emails/téléphones
   └─ Détecte intent signals

JOUR 1 — 18:00 (18h)
└─ System score automatiquement
   ├─ Calcule SaaS Fit (85-95)
   ├─ Assign Priority: 45 P1-P2, 5 P3-P4
   └─ Génère 45 messages (P1-P2)

JOUR 2 — 03:00 AM 🌙
└─ AUTOMATION 3 AM TOURNE!
   ├─ 🕷️  Scrape LinkedIn → 35 nouveaux
   ├─ 📷 Scrape Instagram → 28 nouveaux
   ├─ 🔍 Scrape Google → 42 nouveaux
   └─ TOTAL: 105 nouveaux prospects!

JOUR 2 — 04:00 AM
└─ Auto-enrichment + scoring
   └─ 105 nouveaux prospect scorés

JOUR 2 — 04:30 AM
└─ AUTO-SEND EMAILS! 📧
   └─ 23 "Sourcing & Vetting" emails auto-envoyés

JOUR 2 — 09:00 AM
└─ Follow-ups automatiques
   └─ "Just checking in..." emails

JOUR 2 — 18:00 (18h)
└─ Analytics & Reporting
   └─ Dashboard montre: opens 50%, clicks 30%

JOUR 3-14
└─ Follow-up automatique (j3, j7, j14)
   └─ Suivi sans intervention

JOUR 30
└─ Résultats finaux
   ├─ 2-3 deals fermés ✅
   ├─ 4% conversion rate
   └─ ROI: 50 prospects → €10K-30K revenue
```

---

## 🎯 Paramètres de Configuration

Edit `.env` pour customiser:

```env
# ========= DATABASE =========
DATABASE_URL=postgresql://user:pass@localhost/kucibok

# ========= EMAIL =========
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your@gmail.com
SENDER_NAME=Kucibok
SMTP_PASSWORD=app_password  # Use app password, not real password!

# ========= AUTOMATION =========
SCHEDULER_ENABLED=true
AUTOMATION_HOUR=3  # Run at 3 AM

# ========= SCRAPING (Optional for production) =========
SERPAPI_KEY=your_serpapi_key
APOLLO_API_KEY=your_apollo_key
HUNTER_API_KEY=your_hunter_key
```

---

## 💡 Tips & Tricks

### **Voir les prospects récemment créés**

```powershell
$response = Invoke-WebRequest "http://localhost:8000/api/prospects?status=IDENTIFIED&sort=-created_at"
$json = $response.Content | ConvertFrom-Json
$json.items | Select-Object name,email,country | Format-Table
```

### **Exporter en Excel**

Via dashboard: **Prospects → Export → Excel**

Ou via API:
```powershell
$response = Invoke-WebRequest "http://localhost:8000/api/prospects?prospect_type=CURATOR&limit=500"
$json = $response.Content | ConvertFrom-Json
$json.items | Export-Csv -Path "prospects.csv" -NoTypeInformation
```

### **Tester email avant 3 AM**

```python
from app.services.email_service import EmailService

config = EmailService.get_config_from_env()
service = EmailService(config)

# Envoyer email de test
service.send_email(
    to="curator@gallery.fr",
    subject="Test: Sourcing & Vetting Offer",
    body="Test message..."
)
```

---

## 🔐 Production Checklist

- [ ] `.env` bien configuré (no hardcoded secrets)
- [ ] PostgreSQL prod (não localhost)
- [ ] Redis prod (cloud or self-hosted)
- [ ] SMTP configuré (Gmail app password ou Outlook)
- [ ] Logs configurés (rotation)
- [ ] Database backups (daily)
- [ ] Monitoring actif (email alerts)

---

## 📞 Troubleshooting

### **API ne répond pas?**

```powershell
# Vérifier le port 8000
netstat -ano | findstr :8000

# Tue le processus si nécessaire
taskkill /PID <PID> /F
```

### **Scheduler ne lance pas?**

```powershell
# Vérifier les logs du terminal 3
# Chercher: "Automation scheduler started"

# Vérifier la config
python -c "from app.config import settings; print(settings.scheduler_enabled)"
```

### **Celery worker ne traite pas les jobs?**

```powershell
# Vérifier Redis est connecté
redis-cli ping
# Réponse: PONG

# Vérifier les jobs en attente
celery -A app.workers.celery_app inspect active
```

### **Pas d'emails envoyés?**

```powershell
# Tester SMTP
python -c "
import smtplib
from app.config import settings
smtp = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
smtp.starttls()
smtp.login(settings.smtp_username, settings.smtp_password)
print('✅ SMTP works!')
"
```

---

## 🎯 Étapes Suivantes

1. ✅ **Lancer le système** (3 terminaux)
2. ✅ **Deep source 50 prospects** (1 commande)
3. ✅ **Vérifier dashboard** (http://localhost:3000)
4. ✅ **Attendre 3 AM** (automation démarre)
5. ✅ **Voir résultats le matin** (emails envoyés, réponses tracking)

---

## 🚀 Ready?

```powershell
# Terminal 1
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2
celery -A app.workers.tasks worker --loglevel=info

# Terminal 3
python -m app.scheduler.automated_tasks

# Terminal 4
.\test_deep_source_api.ps1
```

**Voilà! Système lancé! 🎉**

Pendant que vous dormez, Kucibok prospecte pour vous. 🤖

---

## 📊 Dashboard

Après lancement, accédez:
- **API Docs**: http://localhost:8000/docs
- **Dashboard**: http://localhost:3000 (si Node.js configuré)
- **Health Check**: http://localhost:8000/health

---

## 📞 Support

Besoin d'aide?
- Voir logs: `tail -f logs/kucibok.log`
- Vérifier config: `.env` file
- Lire guides: `DEEP_SOURCE_GUIDE.md`, `AUTOMATION_COMPLETE.md`

**Bonne prospection! 🚀**
