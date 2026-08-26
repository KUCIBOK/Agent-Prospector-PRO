# 🚀 Démarrage Rapide - Prospection Manuelle

## ⚡ Voici comment vous allez l'utiliser:

```
TERMINAL 1: Lancer l'API
    ↓
TERMINAL 2: Lancer le Worker Celery
    ↓
NAVIGATEUR: Ouvrir http://localhost:8000/dashboard.html
    ↓
CLIQUER: "🔥 Deep Source Curators"
    ↓
VOIR: Prospects trouvés en temps réel sur le dashboard
```

---

## 🎯 **Étape 1: Terminal 1 - Démarrer l'API FastAPI**

```powershell
cd "C:\Users\Moctar Sidibe\Desktop\Collection art primitif Tomasini\Sculpture\prospecto VA"

python -m uvicorn app.main:app --reload --port 8000
```

**Output attendu:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

✅ **L'API est prête!**

---

## 🎯 **Étape 2: Terminal 2 - Démarrer le Celery Worker**

```powershell
# Dans un NOUVEAU terminal
cd "C:\Users\Moctar Sidibe\Desktop\Collection art primitif Tomasini\Sculpture\prospecto VA"

celery -A app.workers.tasks worker --loglevel=info
```

**Output attendu:**
```
celery@YOUR-MACHINE ready to accept tasks
```

✅ **Le worker est prêt!**

---

## 🎯 **Étape 3: Navigateur - Ouvrir le Dashboard**

Ouvrez dans votre navigateur:

```
http://localhost:8000/dashboard.html
```

ou directement depuis le fichier:
```
file:///C:/Users/Moctar Sidibe/Desktop/Collection art primitif Tomasini/Sculpture/prospecto VA/dashboard.html
```

**Vous verrez:**
- ✅ Statistiques en temps réel (Prospects, Messages, Jobs)
- 🔥 Bouton "Deep Source Curators" pour lancer la prospection
- 🎨 Bouton "Instagram Analysis" pour analyser les artistes
- 💼 Bouton "LinkedIn Monitoring" pour monitorer les curateurs
- ⭐ Bouton "Rescore Artists" pour recalculer les scores

---

## 🔥 **Étape 4: Lancer la Prospection Manuellement**

### **Méthode A: Via le Dashboard (Recommandé)**

1. Allez sur http://localhost:8000/dashboard.html
2. Changez le nombre de prospects à trouver (défaut: 50)
3. Cliquez sur **"🔥 Lancer"**
4. Attendez ~30-60 secondes
5. Vérifiez: Les prospects apparaissent dans la liste!

### **Méthode B: Via Invoke-WebRequest (PowerShell)**

```powershell
# Terminal 3
$response = Invoke-WebRequest `
  -Uri "http://localhost:8000/api/prospects/deep-source?target_count=50" `
  -Method POST

$json = $response.Content | ConvertFrom-Json
Write-Host "✅ Created: $($json.created) prospects"
```

### **Méthode C: Via curl (PowerShell)**

```powershell
curl -X POST "http://localhost:8000/api/prospects/deep-source?target_count=50"
```

---

## 📊 **Vérifier les Résultats**

### **Sur le Dashboard:**
- Les statistiques se mettent à jour automatiquement toutes les 10 secondes
- Les prospects trouvés s'affichent dans "📋 Derniers Prospects"

### **Via l'API Swagger:**

Allez sur: **http://localhost:8000/docs**

Vous pouvez tester tous les endpoints:
- `GET /api/prospects` — Voir tous les prospects
- `POST /api/prospects/deep-source` — Lancer deep source
- `GET /api/monitoring/summary` — Voir les stats
- etc.

---

## 🎯 **Workflow Typique**

### **Jour 1 - 10:00 AM**

```powershell
# Lancer 50 prospects curateurs
POST http://localhost:8000/api/prospects/deep-source?target_count=50

# Résultat:
# ✅ 50 prospects créés
# ⚠️  2 doublons (supprimés)
# 📊 Dashboard montre: Total = 50
```

### **Jour 1 - 14:00 (14h)**

```powershell
# Analyser les artistes trouvés sur Instagram
POST http://localhost:8000/api/monitoring/jobs/analyze-instagram

# Résultat:
# 📷 Scrape Instagram
# 🔔 Détecte signaux d'intention
# ⭐ Update scores artistes
```

### **Jour 1 - 18:00 (18h)**

```powershell
# Monitorer les curateurs sur LinkedIn
POST http://localhost:8000/api/monitoring/jobs/monitor-linkedin

# Résultat:
# 💼 Scrape profils LinkedIn
# 🔔 Détecte changements
# 📈 Update priorités
```

### **Jour 2 - 09:00 AM**

```powershell
# Recalculer les scores des artistes
POST http://localhost:8000/api/monitoring/jobs/rescore-artists-advanced

# Résultat:
# ⭐ Fair Score (0-100)
# 🎨 Gallery Score (0-100)
# 🏆 Awards Score (0-100)
# 📊 Final Score = moyenne pondérée
```

---

## 🛠️ **Troubleshooting**

### **API ne répond pas?**

```powershell
# Vérifier si le port 8000 est utilisé
netstat -ano | findstr :8000

# Tue le processus si nécessaire
taskkill /PID <PID> /F

# Relancer
python -m uvicorn app.main:app --reload --port 8000
```

### **Celery worker ne traite pas les jobs?**

```powershell
# Vérifier Redis
redis-cli ping
# Réponse: PONG

# Vérifier les jobs en attente
celery -A app.workers.tasks inspect active

# Relancer le worker
celery -A app.workers.tasks worker --loglevel=info
```

### **Dashboard affiche "Chargement..." ?**

1. Vérifiez que l'API répond: http://localhost:8000/health
2. Vérifiez les erreurs dans la console du navigateur (F12)
3. Relancez l'API et rafraîchissez la page

### **Deep Source ne trouve pas de prospects?**

```powershell
# Vérifier les logs du Terminal 1 (API)
# Chercher: "🔥 Starting deep source..."

# Vérifier les logs du Terminal 2 (Worker)
# Chercher: "Celery task started"

# Vérifier la base de données
python -c "from app.db import init_db; init_db(); print('✅ DB OK')"
```

---

## 📱 **Commandes Rapides**

### **PowerShell Shortcuts**

Créez un fichier `run-all.ps1`:

```powershell
# Terminal 1
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\Moctar Sidibe\Desktop\Collection art primitif Tomasini\Sculpture\prospecto VA'; python -m uvicorn app.main:app --reload --port 8000"

# Terminal 2
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\Moctar Sidibe\Desktop\Collection art primitif Tomasini\Sculpture\prospecto VA'; celery -A app.workers.tasks worker --loglevel=info"

# Terminal 3
Start-Process powershell -ArgumentList "-NoExit", "-Command", "start http://localhost:8000/dashboard.html"
```

Lancez:
```powershell
.\run-all.ps1
```

---

## ✅ **Checklist Final**

- [ ] Terminal 1: API en cours d'exécution (port 8000)
- [ ] Terminal 2: Celery worker prêt
- [ ] Terminal 3: Navigateur ouvert sur http://localhost:8000/dashboard.html
- [ ] Dashboard affiche les stats (en rafraîchissement)
- [ ] Cliquez sur "🔥 Deep Source Curators" pour commencer!

---

## 🎯 **Prochaines Étapes**

1. ✅ **Démarrer les 2 terminaux** (API + Worker)
2. ✅ **Ouvrir le dashboard**
3. ✅ **Lancer Deep Source** (50 prospects)
4. ✅ **Analyser Instagram**
5. ✅ **Monitorer LinkedIn**
6. ✅ **Rescorer les artistes**
7. ✅ **Voir les résultats sur le dashboard**

---

## 🚀 **Ready?**

```powershell
# Terminal 1
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2 (New PowerShell window)
celery -A app.workers.tasks worker --loglevel=info

# Navigateur
http://localhost:8000/dashboard.html
```

**Voilà! Vous êtes prêt! 🎉**

Cliquez sur **"🔥 Deep Source Curators"** pour lancer la prospection manuelle!

---

## 📞 Support

Besoin d'aide?
- Consultez les logs dans chaque terminal
- Vérifiez la configuration `.env`
- Lisez les guides: `DEEP_SOURCE_GUIDE.md`, `DEPLOYMENT_GUIDE.md`

**Bonne prospection! 🚀**
