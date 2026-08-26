# 📊 Guide du Dashboard - Mode Visuel

## 🎯 Vue d'ensemble

Le dashboard est divisé en **4 sections**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    🚀 Kucibok Prospector                        │
│       Plateforme autonome de prospection - Contrôle Manuel      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┬─────────────────┬──────────────────────────────┐
│ 📊 PROSPECTS    │ ✉️ MESSAGES      │ ⚙️ SYSTÈME                   │
├─────────────────┼─────────────────┼──────────────────────────────┤
│ Total: 0        │ Total: 0        │ Uptime: -                    │
│ Artistes: 0     │ Brouillons: 0   │ Jobs Total: 0                │
│ Clients: 0      │ Envoyés: 0      │ Erreurs: 0                   │
│ P1: 0           │ Répondus: 0     │ Signaux Récents: 0           │
│ P2: 0           │ Meetings: 0     │                              │
└─────────────────┴─────────────────┴──────────────────────────────┘

┌──────────────────────────┬──────────────────────────┬─────────────┐
│ 🔥 DEEP SOURCE CURATORS  │ 🎨 INSTAGRAM ANALYSIS    │ 💼 LINKEDIN │
├──────────────────────────┼──────────────────────────┼─────────────┤
│ Scrape Google            │ Analyser les artistes    │ Monitorer   │
│ Trouver curateurs        │ Détecter signaux         │ les         │
│ [50] [LANCER]            │ [ANALYSER]               │ curateurs   │
│ Status: idle             │ Status: idle             │ [MONITORER] │
└──────────────────────────┴──────────────────────────┴─────────────┘

┌──────────────────────────┬──────────────────────────┐
│ ⭐ RESCORE ARTISTS       │ 🔄 ACTIONS SUPPLÉMENTAIRES│
├──────────────────────────┼──────────────────────────┤
│ Recalculer les scores    │ Rafraîchir               │
│ Fair + Gallery + Awards  │ Health Check             │
│ [RESCORER]               │ [RAFRAÎCHIR]  [VÉRIFIER] │
│ Status: idle             │                          │
└──────────────────────────┴──────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 📋 DERNIERS PROSPECTS TROUVÉS (Top 10)                          │
├─────────────────────────────────────────────────────────────────┤
│ Chargement...                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Section 1: Statistiques (Auto-Actualisées)

Affiche les **statistiques en temps réel** (mise à jour toutes les 10 secondes):

### 📊 PROSPECTS
```
Total         : 50      (Nombre total de prospects)
🎨 Artistes   : 15      (Prospects de type ARTIST)
🎯 Clients    : 35      (Curateurs, galeries, advisors)
P1 (Hot)      : 20      (Priorité critique - à contacter)
P2            : 15      (Priorité haute - suivi)
```

### ✉️ MESSAGES
```
Total         : 30      (Nombre total de messages générés)
📝 Brouillons : 10      (Pas encore envoyés)
✅ Envoyés    : 20      (Emails envoyés)
💬 Répondus   : 5       (Prospects qui ont répondu)
📅 Meetings   : 2       (Meetings confirmés)
```

### ⚙️ SYSTÈME
```
Uptime        : 2h 15m  (Temps depuis le lancement)
Jobs Total    : 25      (Nombre total de jobs traités)
❌ Erreurs    : 0       (Nombre d'erreurs)
🔔 Signaux    : 8       (Signaux d'intention détectés)
```

---

## 🔥 Section 2: Actions Manuelles

### **ACTION 1️⃣: 🔥 Deep Source Curators**

**Qu'est-ce que c'est?**
- Scrape **Google** pour trouver des curateurs indépendants
- Extrait noms, emails, websites
- Importe dans la base de données
- Crée des prospects avec status **IDENTIFIED**

**Comment l'utiliser:**

1. Changez la valeur du nombre de prospects (défaut: **50**)
   ```
   [50] ← Nombre à trouver
   ```

2. Cliquez sur **"Lancer"** (bouton violet)

3. Attendez le résultat (typiquement 30-60 secondes)
   ```
   Scraping en cours...
   (spinner animé)
   ```

4. Voyez le résultat:
   ```
   ✅ Created: 50 prospects!
   ⚠️  Duplicates: 2 removed
   Errors: 0
   ```

5. Les prospects apparaissent dans la section "📋 Derniers Prospects"

**Résultat attendu:**
- 50 nouveaux prospects créés
- Status: IDENTIFIED
- Prêts pour enrichissement

---

### **ACTION 2️⃣: 🎨 Instagram Analysis**

**Qu'est-ce que c'est?**
- Analyse les **artistes trouvés** sur Instagram
- Détecte les signaux d'intention (posts, hashtags, engagement)
- Met à jour les scores des artistes
- Identifie les artistes prometteurs

**Comment l'utiliser:**

1. Assurez-vous qu'il y a des prospects importés (Action 1)

2. Cliquez sur **"Analyser"** (bouton violet)

3. Attendez (typiquement 5-10 minutes)
   ```
   Analyse en cours...
   (spinner animé)
   ```

4. Voyez le résultat:
   ```
   ✅ Job queued: abc123def456
   ```

5. Le system traite les jobs en arrière-plan:
   - Scrape les profils Instagram
   - Analyse les posts récents
   - Détecte les engagement patterns
   - Met à jour les scores

**Résultat attendu:**
- Instagram data collectée pour chaque artiste
- Signaux d'intention détectés
- Scores artistes mis à jour
- Prospects re-prioritisés

---

### **ACTION 3️⃣: 💼 LinkedIn Monitoring**

**Qu'est-ce que c'est?**
- Monitore les **curateurs** sur LinkedIn
- Détecte les changements (changement de galerie, nouvelle expo, etc.)
- Met à jour les intent signals
- Identifie les bonnes opportunités

**Comment l'utiliser:**

1. Assurez-vous qu'il y a des prospects curateurs (Action 1)

2. Cliquez sur **"Monitorer"** (bouton violet)

3. Attendez (typiquement 5-10 minutes)
   ```
   Monitoring en cours...
   (spinner animé)
   ```

4. Voyez le résultat:
   ```
   ✅ Job queued: xyz789uvw456
   ```

5. Le système traite les jobs en arrière-plan:
   - Scrape les profils LinkedIn
   - Détecte les changements de poste
   - Identifie les nouvelles expositions
   - Met à jour les priorités

**Résultat attendu:**
- LinkedIn data collectée pour chaque curateur
- Changements détectés
- Signaux d'intention mis à jour
- Prospects re-prioritisés

---

### **ACTION 4️⃣: ⭐ Rescore Artists**

**Qu'est-ce que c'est?**
- Recalcule les scores des **artistes** avec l'algorithme avancé
- Utilise 3 critères:
  - **Fair Score** (0-100): Potentiel artistique
  - **Gallery Score** (0-100): Visibilité en galerie
  - **Awards Score** (0-100): Reconnaissances obtenues
- Calcule un **Final Score** (moyenne pondérée)

**Comment l'utiliser:**

1. Assurez-vous qu'il y a des prospects artistes (Action 1 + Action 2)

2. Cliquez sur **"Rescorer"** (bouton violet)

3. Attendez (typiquement 2-3 minutes)
   ```
   Rescoring en cours...
   (spinner animé)
   ```

4. Voyez le résultat:
   ```
   ✅ Job queued: rst123ijk456
   ```

5. Le système traite les jobs en arrière-plan:
   - Calcule le Fair Score (potentiel artistique)
   - Calcule le Gallery Score (visibilité)
   - Calcule le Awards Score (reconnaissances)
   - Calcule le Final Score
   - Met à jour les priorités en fonction des scores

**Résultat attendu:**
- Tous les artistes reçoivent de nouveaux scores
- Les meilleures prospects remontent (P1, P2)
- Les moins bonnes descendent (P3, P4)
- Les statistiques se mettent à jour

---

### **ACTIONS 5-6: Actions Supplémentaires**

#### 🔄 **Rafraîchir**
- Met à jour **manuellement** les statistiques
- Utile si vous voulez voir les résultats immédiatement
- Normalement, c'est auto-actualisé toutes les 10 secondes

#### 📡 **Health Check**
- Vérifie que l'API répond
- Affiche la version du système
- Utile pour troubleshooting

---

## 📋 Section 3: Derniers Prospects Trouvés

Affiche les **10 derniers prospects importés**:

```
┌─────────────────────────────────────────────────────────────┐
│ 📋 DERNIERS PROSPECTS TROUVÉS (Top 10)                      │
├─────────────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────────────────┐    │
│ │ Marie Dubois                     (CURATOR)           │    │
│ │ 📧 marie@galerie.fr                                 │    │
│ │ 🌐 https://galerie.fr                               │    │
│ │ ⚡ Priority: P1                                      │    │
│ └──────────────────────────────────────────────────────┘    │
│ ┌──────────────────────────────────────────────────────┐    │
│ │ Jean Pierre Morel               (ARTIST)             │    │
│ │ 📧 jp@morelart.com                                  │    │
│ │ 🌐 https://morelart.com                             │    │
│ │ ⚡ Priority: P2                                      │    │
│ └──────────────────────────────────────────────────────┘    │
│ ...                                                         │
└─────────────────────────────────────────────────────────────┘
```

**Affichage:**
- **Nom** du prospect
- **Type** (CURATOR, ARTIST, GALLERY, ART_ADVISOR)
- **Email** (📧)
- **Website** (🌐)
- **Priority** (⚡ P1/P2/P3/P4)

---

## ⚠️ Section 4: Journal d'Erreurs

Si des erreurs se produisent, elles apparaissent ici:

```
┌─────────────────────────────────────────────────────────────┐
│ ⚠️  JOURNAL D'ERREURS                                        │
├─────────────────────────────────────────────────────────────┤
│ Deep Source Error                                           │
│ Connection timeout to Google Search                         │
│ 14:23:45                                                    │
│                                                             │
│ Instagram Analysis Error                                   │
│ Rate limit exceeded - retry after 60 seconds               │
│ 14:25:12                                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Workflow Typique (Jour 1)

### **10:00 AM**
1. Allez sur http://localhost:8000/dashboard.html
2. Cliquez sur "🔥 Deep Source Curators"
3. Mettez **50** dans le champ
4. Cliquez **"Lancer"**
5. Attendez 30-60 secondes
6. ✅ 50 prospects trouvés!

**Dashboard montre:**
```
Total: 50, P1: 20, P2: 15
Prospects: Marie Dubois, Jean Pierre, ...
```

### **14:00 (14h)**
1. Cliquez sur "🎨 Instagram Analysis"
2. Attendez 5-10 minutes
3. ✅ Artistes analysés!

**Dashboard montre:**
```
Signaux Récents: 8 (nouvelles signals détectées)
Scores mis à jour
```

### **18:00 (18h)**
1. Cliquez sur "💼 LinkedIn Monitoring"
2. Attendez 5-10 minutes
3. ✅ Curateurs monitorés!

**Dashboard montre:**
```
Prospects re-prioritisés basé sur LinkedIn data
P1 count peut augmenter si changements détectés
```

### **Jour 2 - 09:00 AM**
1. Cliquez sur "⭐ Rescore Artists"
2. Attendez 2-3 minutes
3. ✅ Scores recalculés!

**Dashboard montre:**
```
Tous les scores mises à jour
Fair Score: 87, Gallery Score: 92, Awards Score: 95
Final Score: 91
```

---

## 💡 Tips & Tricks

### **Tip 1: Auto-Actualisation**
Le dashboard se met à jour automatiquement toutes les 10 secondes. Vous n'avez rien à faire!

### **Tip 2: Voir les Erreurs**
Si quelque chose ne fonctionne pas:
1. Ouvrez la console du navigateur (F12)
2. Allez dans l'onglet "Console"
3. Vous verrez les erreurs d'API

### **Tip 3: Tester Rapidement**
Pour tester avec peu de prospects:
1. Changez la valeur à **5** au lieu de **50**
2. Cliquez "Lancer"
3. Attendez 5-10 secondes
4. Les 5 prospects s'affichent

### **Tip 4: Monitorer les Logs**
Dans les terminaux:
- **Terminal 1 (API)**: Vous voyez les requêtes HTTP
- **Terminal 2 (Worker)**: Vous voyez les jobs Celery

### **Tip 5: Vérifier la Santé du Système**
Cliquez régulièrement sur "📡 Health Check" pour être sûr que l'API répond

---

## ❌ Troubleshooting

### **Problème: "Erreur: xhr failed"**
```
❌ API ne répond pas

Solution:
1. Vérifiez que Terminal 1 (API) est en cours d'exécution
2. Vérifiez que le port 8000 est libre
3. Relancez l'API
4. Rafraîchissez le navigateur
```

### **Problème: "Job queued" mais rien ne se passe**
```
❌ Worker ne traite pas les jobs

Solution:
1. Vérifiez que Terminal 2 (Worker) est en cours d'exécution
2. Vérifiez que Redis fonctionne: redis-cli ping
3. Relancez le Worker
4. Attendez 5-10 secondes
```

### **Problème: Deep Source ne trouve rien**
```
❌ Scraping échoue

Solution:
1. Vérifiez les logs du Terminal 1
2. Cherchez: "🔥 Starting deep source..."
3. Vérifiez votre connexion Internet
4. Essayez avec un nombre moins élevé (10 au lieu de 50)
```

### **Problème: Dashboard affiche "Chargement..." en permanence**
```
❌ API ne répond pas

Solution:
1. Cliquez sur "📡 Health Check"
2. Si ça ne fonctionne pas, l'API est down
3. Allez sur http://localhost:8000/health
4. Vous devez voir: {"status": "ok"}
5. Si non, relancez l'API
```

---

## 🚀 Raccourcis Utiles

### **Dans le Navigateur**
- F5: Rafraîchir la page
- F12: Ouvrir les DevTools (voir les erreurs)
- Ctrl+Shift+J: Console du navigateur

### **Dans les Terminaux**
- Ctrl+C: Arrêter le processus
- ↑: Récupérer la dernière commande
- Ctrl+L: Effacer l'écran

---

## 📞 Support

Si vous avez des problèmes:

1. **Consultez les logs** dans les terminaux
2. **Ouvrez les DevTools** (F12) pour voir les erreurs API
3. **Relancez le système**: Ctrl+C dans chaque terminal, puis relancez
4. **Lisez les guides**: QUICK_START_MANUAL.md, DEEP_SOURCE_GUIDE.md

**Vous êtes prêt! 🚀**

Allez sur http://localhost:8000/dashboard.html et commencez!
