# 🚀 DÉPLOIEMENT RENDER.COM - GUIDE COMPLET

## ✅ AVANTAGES RENDER vs HEROKU

| Feature | Render | Heroku |
|---------|--------|--------|
| **Free Tier** | 750h/mois ✅ | 550h/mois |
| **Database** | PostgreSQL FREE ✅ | Payant ($9/mois) |
| **Performance** | Meilleur ✅ | Ralenti après inactivité |
| **Setup** | Plus simple ✅ | Plus complexe |
| **24/7 Running** | OUI ✅ | OUI |
| **Price** | FREE tier good ✅ | Cher pour production |

---

## 📋 PRÉREQUIS

- [ ] Compte GitHub (recommandé pour auto-deploy)
- [ ] Compte Render.com (gratuit)
- [ ] Git installé
- [ ] 10 minutes

---

## 🎯 STEP 1: Préparer le code (LOCAL)

### 1.1 Vérifier requirements.txt
```bash
cat requirements.txt
# Doit avoir: fastapi, uvicorn, sqlmodel, sqlalchemy, psycopg[binary]
```

### 1.2 Créer .env.local (pour tests locaux)
```bash
cat > .env.local << 'EOF'
ENVIRONMENT=development
DATABASE_URL=sqlite:///./test.db
API_HOST=0.0.0.0
API_PORT=8000
EOF
```

### 1.3 Tester localement
```bash
python -m uvicorn app.main:app --reload
# Doit être accessible sur http://localhost:8000
```

---

## 🎯 STEP 2: Préparer pour Render

### 2.1 Créer .gitignore (si pas existe)
```bash
cat > .gitignore << 'EOF'
.env
.env.local
.env.production
__pycache__/
*.pyc
*.db
*.sqlite
*.sqlite3
.pytest_cache/
.venv/
venv/
env/
node_modules/
.DS_Store
EOF
git add .gitignore
```

### 2.2 Commit les changes
```bash
git add requirements.txt render.yaml
git commit -m "chore: Add Render deployment config"
git push origin main  # ou master
```

---

## 🎯 STEP 3: Connecter GitHub à Render

### 3.1 Aller sur Render.com
```
1. Aller sur https://render.com
2. Click "Sign Up" (ou Sign In si vous avez déjà un compte)
3. Connectez avec GitHub (RECOMMANDÉ pour auto-deploy)
```

### 3.2 Autoriser Render
```
1. GitHub demande permission → Click "Authorize"
2. Render va lire vos repos
```

---

## 🎯 STEP 4: Créer le Service Render

### 4.1 Créer via Blueprint (FACILE)
```
1. Dashboard Render → "New +" → "Blueprint"
2. Sélectionner votre repo GitHub
3. Choisir la branche (main ou master)
4. Click "Deploy"
```

### 4.2 OU créer manuellement (ÉTAPES)

#### A) Créer Web Service
```
1. Render Dashboard → "New +" → "Web Service"
2. Connecter GitHub
3. Sélectionner repo "Collection art primitif..."
4. Paramètres:
   - Name: kucibok-prospector
   - Runtime: Python 3.11
   - Build: pip install -r requirements.txt
   - Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   - Plan: Free
5. Click "Create Web Service"
```

#### B) Créer Database PostgreSQL
```
1. Render Dashboard → "New +" → "PostgreSQL"
2. Paramètres:
   - Name: kucibok-db
   - Database: kucibok_prospector
   - User: kucibok_user
   - Region: Frankfurt (ou proche de vous)
   - Plan: Free
3. Click "Create Database"
```

#### C) Connecter Database au Service
```
1. Aller dans Web Service "kucibok-prospector"
2. "Environment" → "Add Environment Variable"
3. Key: DATABASE_URL
4. Value: (copier depuis PostgreSQL service details)
5. Click "Save"
```

---

## 🎯 STEP 5: Configurer Variables d'Environnement

Dans Render Dashboard → Web Service → Environment:

```
ENVIRONMENT = production
API_HOST = 0.0.0.0
API_PORT = 8000
ENABLE_SCHEDULER = true
ENABLE_EMAIL_TRACKING = true
SMTP_SERVER = smtp.gmail.com (optionnel)
```

---

## ✅ VÉRIFIER LE DÉPLOIEMENT

### Option 1: Dashboard Render
```
1. Aller sur https://render.com/dashboard
2. Cliquer sur "kucibok-prospector" (Web Service)
3. Voir "Live" status
4. Cliquer le lien bleu pour accéder à l'app
```

### Option 2: Tester l'API
```bash
# Remplacer YOUR_URL par l'URL Render
curl https://YOUR_URL.onrender.com/health

# Doit répondre:
# {"status":"healthy","version":"1.0.0"}
```

### Option 3: Voir les Logs
```
1. Service Render → "Logs"
2. Voir les erreurs/succès du déploiement
```

---

## 🔄 AUTO-DEPLOY (OPTIONNEL)

Render déploie automatiquement quand vous push sur GitHub:

```bash
# Faire changes
git add .
git commit -m "feat: Add new email template"
git push origin main

# Render détecte et re-déploie automatiquement! ✅
```

---

## 📊 MONITORER 24/7

### Dashboard Render
- **Logs**: Voir tout ce qui se passe
- **Metrics**: CPU, RAM, Request rate
- **Health Checks**: Automatiques

### Votre App
```bash
# Accéder via:
https://kucibok-prospector.onrender.com

# Dashboard:
https://kucibok-prospector.onrender.com/dashboard

# API:
https://kucibok-prospector.onrender.com/api/prospects
```

---

## 💾 MIGRER LES DONNÉES

Vos prospects SQLite locaux → PostgreSQL Render:

### Option 1: Dump & Restore
```bash
# Exporter data locale
sqlite3 prospects.db ".dump" > dump.sql

# Importer dans Render Postgres (si besoin)
# Via Render console
```

### Option 2: Recréer via API
```bash
# Dans votre app Render, les 76 prospects seront créés
# en exécutant recreate_75_prospects.py via endpoint
```

---

## 🔒 SÉCURITÉ

### Ne JAMAIS commiter:
```
❌ .env (fichier local)
❌ Mots de passe
❌ API keys
❌ Credentials
```

### À la place:
```
✅ .env.example (template vide)
✅ Variables Render Environment
✅ Secrets Management Render
```

---

## 🚨 TROUBLESHOOTING

### Problem: "Build failed"
```
Solution:
1. Vérifier Python 3.11 dans runtime.txt
2. Vérifier requirements.txt syntax
3. Voir les logs Render pour erreurs
```

### Problem: "Database connection error"
```
Solution:
1. Vérifier DATABASE_URL dans Environment
2. Vérifier PostgreSQL service est running
3. Relancer le service
```

### Problem: "App crashes after deploy"
```
Solution:
1. Voir les Logs pour erreur exacte
2. Vérifier app.main.py fonctionne localement
3. Relancer le service via Render Dashboard
```

### Problem: "Port déjà utilisé"
```
Solution:
✅ Render automatiquement assigne $PORT
✅ Notre config utilise $PORT → pas de problème
```

---

## 📞 NEXT STEPS

### Après déploiement:
1. ✅ Tester l'API endpoint
2. ✅ Vérifier logs
3. ✅ Lancer Batch 3 depuis Render
4. ✅ Monitorer en temps réel

### Pour automation 24/7:
```bash
# Créer un endpoint scheduler dans app/main.py
# Qui lance les emails automatiquement
```

---

## 🎉 VOUS ÊTES LIVE!

```
✅ App running on: https://kucibok-prospector.onrender.com
✅ Database: PostgreSQL sur Render
✅ Auto-deploy: Activé via GitHub
✅ 24/7 monitoring: Activé
✅ FREE tier: Illimité (750h/mois)

Prochaine étape:
→ Tester le système Render
→ Continuer vos emails Batch 3
→ Monitorer les réponses
→ Fermer des deals! 🎯
```

---

## 📋 CHECKLIST DÉPLOIEMENT

```
[ ] Code prêt (requirements.txt ✅)
[ ] render.yaml créé ✅
[ ] GitHub repo prêt
[ ] Compte Render créé
[ ] Database PostgreSQL créée
[ ] Environment variables configurées
[ ] Web Service en "Live"
[ ] API accessible
[ ] Logs checking (no errors)
[ ] Données migrées ou recréées
[ ] 24/7 monitoring activé
```

**Status: PRÊT À DÉPLOYER! 🚀**
