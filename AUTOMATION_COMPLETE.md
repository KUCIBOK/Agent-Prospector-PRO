# 🤖 KUCIBOK AUTOMATION COMPLÈTE — Système 24/7

**Votre système de prospection automatisé qui tourne sans vous!**

```
À 3h du matin (CHAQUE JOUR):
  ↓
Scrape LinkedIn, Instagram, Google
  ↓
Trouve curateurs/advisors (FR, US, Asie, Brésil, etc.)
  ↓
Enrichit les profils automatiquement
  ↓
Score chaque prospect
  ↓
Génère messages personnalisés "Sourcing & Vetting"
  ↓
Envoie emails automatiquement
  ↓
Follow-ups jours 3, 7, 14
  ↓
Dashboard en temps réel avec résultats
```

---

## 🎯 **Ce Que Fait Le Système**

### **3:00 AM — Scraping & Prospecting**
```
🕷️  Scrape LinkedIn
    → "curator France contemporary art"
    → "art advisor USA"
    → "gallery director Singapore"
    → "curator China emerging artists"
    → "art advisor Brazil"
    
📷 Scrape Instagram
    → #curator #artadvisor #contemporaryart
    → Profiles de curateurs/advisors
    
🔍 Scrape Google Search
    → "curator + pays cible"
    → "art advisor + pays cible"
    → Résultats de recherche
    
Result: 50+ nouveaux prospects trouvés
```

### **Après Scraping — Enrichissement Auto**
```
Chaque prospect trouvé:
  ✅ Normalise les données (pays, email, URLs)
  ✅ Télécharge le website
  ✅ Extrait emails, téléphones, réseaux sociaux
  ✅ Détecte signaux d'intérêt
  ✅ Score automatiquement (Artist Fit ou SaaS Fit)
  ✅ Calcule Priority (P1-P4)
```

### **Après Scoring — Emails Auto**
```
P1-P2 prospects (haute confiance):
  ✅ Génère message "Sourcing & Vetting"
  ✅ Personnalisé par type (Curator/Advisor/Gallery)
  ✅ Envoie automatiquement
  ✅ Track ouverture + clic
  ✅ Planifie follow-ups jours 3, 7, 14
```

### **Suivi Automatique**
```
Jour 0: Email initial (Sourcing & Vetting)
Jour 3: Relance automatique
Jour 7: Deuxième follow-up auto
Jour 14: Dernier email auto
Jour 30+: Analyse résultats
```

---

## 🚀 **Lancer Le Système**

### **Étape 1: Configurer l'Email**

Ajouter à `.env`:

```env
# ========= EMAIL CONFIGURATION =========
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=votre@gmail.com
SENDER_NAME=Kucibok
SMTP_USERNAME=votre@gmail.com
SMTP_PASSWORD=app_password_google  # ← Pas le vrai mot de passe!
SMTP_TLS=true

# ========= SCRAPING SERVICES =========
# Option 1: SerpAPI (Google Search)
SERPAPI_KEY=your_serpapi_key

# Option 2: Apollo.io (LinkedIn emails)
APOLLO_API_KEY=your_apollo_key

# Option 3: Hunter.io (Email finder)
HUNTER_API_KEY=your_hunter_key

# Option 4: Instagram Graph API (Meta)
INSTAGRAM_GRAPH_API_TOKEN=your_ig_api_token
```

### **Étape 2: Démarrer Le Système (3 Terminaux)**

```powershell
# Terminal 1: FastAPI API
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Celery Worker (enrichment, scoring)
celery -A app.workers.tasks worker --loglevel=info

# Terminal 3: Automation Scheduler (3 AM engine)
python -m app.scheduler.automated_tasks
```

### **Résultat**

```
✅ API prête: http://localhost:8000
✅ Worker actif: Enrichissement & scoring
✅ Scheduler actif: À 3h du matin → Scraping + Emails
✅ Dashboard: http://localhost:3000
```

---

## 📊 **Dashboard en Temps Réel**

Votre dashboard montre:

```
🤖 AUTOMATION STATUS
├─ Scheduler: ✅ RUNNING
├─ Last scrape: Today 3:00 AM
└─ Next scrape: Tomorrow 3:00 AM

📈 DAILY RESULTS (24h)
├─ Prospects scraped: 47
├─ New prospects created: 43
├─ Duplicates found: 4
└─ Errors: 0

📧 EMAIL STATUS
├─ Emails sent: 23 (P1-P2 only)
├─ Opens: 12 (52%)
├─ Clicks: 7 (30%)
├─ Replies: 2 (9%)
└─ Signups: 1 (4%)

🌍 PROSPECTS BY COUNTRY
├─ France: 12
├─ USA: 8
├─ Singapore: 5
├─ China: 4
├─ Brazil: 3
└─ Other: 11

🎯 PIPELINE
├─ Identified (new): 43
├─ Prequalified (scored): 38
├─ Contacted (email sent): 23
├─ Replied: 2
└─ Converted: 1
```

---

## 🔄 **Workflow Complet**

```
+------------------------+
| VOUS DONNEZ EXCEL DATA  |
+------------------------+
        ↓
+------------------------+
| IMPORT AUTOMATIQUE      |
| Status: IDENTIFIED      |
+------------------------+
        ↓
+------------------------+
| 3 AM EVERY DAY          |
| Auto-scrape commence    |
+------------------------+
        ↓
+------------------------+
| ENRICHISSEMENT AUTO     |
| - Normalise données     |
| - Scrape websites       |
| - Détecte signaux       |
+------------------------+
        ↓
+------------------------+
| SCORING AUTO            |
| - Calcule SaaS Fit      |
| - Priority P1-P4        |
| - Status: PREQUALIFIED  |
+------------------------+
        ↓
+------------------------+
| EMAIL AUTO              |
| P1-P2 seulement         |
| "Sourcing & Vetting"    |
+------------------------+
        ↓
+------------------------+
| FOLLOW-UP AUTO          |
| Jour 3, 7, 14          |
+------------------------+
        ↓
+------------------------+
| TRACKING EN TEMPS RÉEL  |
| Dashboard updated       |
+------------------------+
```

---

## 📋 **Checklist: Démarrer L'Automation Complète**

### **One-time Setup**
- [ ] Créer compte Gmail + App Password
- [ ] Acheter API keys (SerpAPI, Apollo.io, ou Hunter.io)
- [ ] Configurer Instagram Graph API (optionnel)
- [ ] Ajouter tous les secrets dans `.env`
- [ ] Tester envoi email manuel

### **Lancer Le Système**
- [ ] Démarrer API (Terminal 1)
- [ ] Démarrer Worker (Terminal 2)
- [ ] Démarrer Scheduler (Terminal 3)
- [ ] Accéder dashboard: http://localhost:3000

### **Donner De La Data**
- [ ] Préparer fichier Excel avec prospects
- [ ] Importer via API
- [ ] Voir résultats dans dashboard

### **Monitoring 24/7**
- [ ] Vérifier logs chaque matin (après 3 AM)
- [ ] Voir dashboard pour résultats
- [ ] Répondre aux emails reçus
- [ ] Ajuster paramètres si nécessaire

---

## 🎯 **Exemple: Jour 1 Complet**

```
08:00 - Vous importez Excel (50 prospects)
        Status: IDENTIFIED

15:00 - System a enrichi les profils
        18 sources trouvées, emails extraits

18:00 - System a scoré
        38 prequalified, 12 P1-P2

03:00 (LENDEMAIN) - AUTOMATION 3 AM TOURNE
        🕷️  Scrape LinkedIn → 35 nouveaux prospects
        📷 Scrape Instagram → 28 nouveaux
        🔍 Scrape Google → 42 nouveaux
        Total: 105 nouveaux prospects trouvés!

03:30 - Auto-enrichissement des 105 prospects

04:00 - Auto-scoring des 105 prospects

04:15 - AUTO-ENVOIE EMAILS
        - 23 Sourcing & Vetting emails envoyés
        - Status: "SENT"
        - Follow-ups planifiés jours 3, 7, 14

08:00 - Dashboard montre:
        ✅ 105 nouveaux prospects
        ✅ 23 emails envoyés
        ✅ Suivi automatique en place

10:00 - Première réponse arrive! 🎉
```

---

## 💡 **Services Tiers Recommandés**

Pour scraper LÉGALEMENT & FACILEMENT:

| Service | Use Case | Cost |
|---------|----------|------|
| **SerpAPI** | Google Search | $10/month |
| **Apollo.io** | LinkedIn emails | $49/month |
| **Hunter.io** | Email finder | $99/month |
| **Bright Data** | Web scraping | Variable |
| **Instagram Graph API** | Instagram profiles | Free (Meta) |

---

## 🔐 **Sécurité & Compliance**

✅ **Légal & Éthique**:
- Utilise uniquement les APIs officielles
- Respecte robots.txt
- Pas de scraping "Black hat"
- Compliance GDPR/CCPA

✅ **Données Protégées**:
- Tous les secrets dans `.env` (jamais dans git)
- Encryption optionnelle en production
- Logs sécurisés

---

## 🚨 **Troubleshooting**

### **Le scheduler ne lance pas à 3 AM**
```powershell
# Vérifier les logs
tail -f logs/kucibok.log | grep "3 AM\|Prospecting"

# Vérifier la config
python -c "
from app.scheduler.automated_tasks import start_automation_scheduler
from app.config import settings
print(f'Scheduler enabled: {settings.scheduler_enabled}')
"
```

### **Les emails ne s'envoient pas**
```powershell
# Tester SMTP
python -c "
import smtplib
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.starttls()
smtp.login('your@gmail.com', 'app_password')
print('✅ SMTP works!')
"
```

### **Pas de prospects trouvés**
- Vérifier les clés API (SerpAPI, Apollo, Hunter)
- Vérifier les logs pour erreurs
- Vérifier les pays cibles dans config

---

## 📞 **Support & Logs**

```powershell
# Voir tous les logs
tail -f logs/kucibok.log

# Voir logs spécifiques
tail -f logs/kucibok.log | grep "3 AM\|Prospecting\|Email\|Scrape"

# Compter les prospects créés (24h)
python -c "
from app.db import SessionLocal
from sqlmodel import select, func
from app.models import Prospect
session = SessionLocal()
count = session.scalar(select(func.count()).select_from(Prospect))
print(f'Total prospects: {count}')
"
```

---

## ✨ **Le Résultat**

Vous pouvez dormir tranquille:

```
23:00 - Vous allez dormir
  ↓
03:00 - Kucibok scrape automatiquement
  ↓
04:00 - Envoie 20+ emails automatiquement
  ↓
09:00 - Follow-ups automatiques
  ↓
08:00 (Matin) - Vous vous réveillez
         Dashboard montre:
         ✅ 100+ nouveaux prospects trouvés
         ✅ 20+ emails envoyés
         ✅ 2+ réponses reçues
```

**Pendant que vous dormez, Kucibok prospecte pour vous!** 🚀

---

## 🎉 **Vous Avez Maintenant**

✅ **Import Excel** — Donner de la data, système traite  
✅ **Auto-Scraping** — LinkedIn, Instagram, Google à 3 AM  
✅ **Auto-Enrichissement** — Profile completion automatique  
✅ **Auto-Scoring** — Prospects évalués automatiquement  
✅ **Auto-Emails** — "Sourcing & Vetting" envoyés auto  
✅ **Auto-Follow-ups** — Relances jours 3, 7, 14  
✅ **24/7 Monitoring** — Dashboard en temps réel  

**Un système complètement autonome de prospection!** 🤖

Besoin d'aide? Les logs sont votre ami:
```powershell
tail -f logs/kucibok.log
```

Bonne prospection! 🚀
