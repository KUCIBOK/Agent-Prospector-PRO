# 📋 SETUP GIT & GITHUB - Pour Render Deploy

## ÉTAPE 1: Initialiser Git (si pas fait)

```bash
cd "C:\Users\Moctar Sidibe\Desktop\Collection art primitif Tomasini\Sculpture\prospecto VA"

# Vérifier si git est init
git status

# Si erreur "not a git repository", faire:
git init
git config user.name "Kucibok"
git config user.email "kucibok221@gmail.com"
```

---

## ÉTAPE 2: Préparer .gitignore

```bash
# Créer/vérifier .gitignore
cat > .gitignore << 'EOF'
# Environment
.env
.env.local
.env.production
.env*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
.venv/
venv/
ENV/
env/

# Database
*.db
*.sqlite
*.sqlite3
prospects.db
test.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Logs
*.log
logs/

# Env files (keep example)
.env
!.env.example
EOF
```

---

## ÉTAPE 3: Ajouter fichiers Render

```bash
# Ces fichiers doivent être dans le repo
git add render.yaml
git add requirements.txt
git add .gitignore
git add .env.example
git add RENDER_QUICK_START.md
git add HEROKU_RENDER_DEPLOYMENT.md
```

---

## ÉTAPE 4: Premier Commit

```bash
git commit -m "chore: Add Render deployment configuration

- Add render.yaml for Web Service & Database setup
- Add requirements.txt with all dependencies
- Add .gitignore for security
- Add deployment guides"
```

---

## ÉTAPE 5: Créer/Connecter GitHub (Si pas existe)

### A) Si vous avez déjà un GitHub repo:
```bash
git remote add origin https://github.com/YOUR_USERNAME/repository-name.git
git branch -M main
git push -u origin main
```

### B) Si vous n'avez PAS de GitHub:

1. **Créer repo sur GitHub:**
   ```
   1. Aller sur https://github.com/new
   2. Repository name: kucibok-prospector
   3. Description: "AI-powered Paris prospecting system"
   4. Click "Create repository"
   ```

2. **Pousser votre code:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/kucibok-prospector.git
   git branch -M main
   git push -u origin main
   ```

---

## ✅ VÉRIFIER

```bash
# Vérifier que tout est commit
git status
# Doit dire: "On branch main - nothing to commit"

# Vérifier le remote
git remote -v
# Doit montrer: origin https://github.com/YOUR_USERNAME/kucibok-prospector.git
```

---

## 🎯 MAINTENANT: Déployer sur Render

1. **Aller sur https://render.com**
2. **Sign Up avec GitHub** (IMPORTANT!)
3. **Click "New +" → "Blueprint"**
4. **Sélectionner votre repo kucibok-prospector**
5. **Click "Deploy"**

Render va tout configurer automatiquement! ✅

---

## 📊 AUTO-DEPLOY EN FUTUR

Maintenant que vous êtes connecté:
- Chaque fois que vous faites `git push`
- Render détecte le changement
- Re-déploie automatiquement
- Zéro downtime! 🎉

```bash
# Exemple future:
git add .
git commit -m "feat: Add new email template"
git push origin main
# → Render redéploie automatiquement!
```

---

## 🔒 SÉCURITÉ - IMPORTANT!

### NE JAMAIS commiter:
```
❌ .env (avec vraies valeurs)
❌ Mots de passe
❌ API keys
❌ Secrets
```

### À la place:
```
✅ .env.example (vide comme template)
✅ Variables dans Render Dashboard
```

Si vous avez des secrets:
1. Ajouter à `.gitignore`
2. Mettre dans Render Environment
3. App va les lire via `os.environ.get()`

---

## ✅ CHECKLIST GIT SETUP

```
[ ] Git installé?
[ ] Repository initialisé?
[ ] .gitignore créé?
[ ] Fichiers Render added (render.yaml, requirements.txt)?
[ ] Premier commit fait?
[ ] GitHub repo créé?
[ ] Push vers GitHub réussi?
[ ] GitHub + Render connectés?
```

---

## 🚀 RÉSUMÉ

```
LOCAL:                          GITHUB:                    RENDER:
┌──────────────────┐           ┌──────────────┐          ┌──────────────┐
│  Your Code       │ git push  │ Your Repo    │ auto     │  Live App!   │
│  + render.yaml   │ ──────→   │  kucibok-    │ deploy   │              │
│  + requirements  │           │  prospector  │ ─────→   │ 24/7 running │
└──────────────────┘           └──────────────┘          └──────────────┘
```

**Status: PRÊT À DÉPLOYER! 🎯**
