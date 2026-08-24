# 🎯 KUCIBOK BRIDGE PLAYBOOK — Système Intégré

**Votre système de prospection fonctionne MAINTENANT avec le playbook Kucibok Bridge complet!**

```
Playbook Kucibok Bridge:
  ├─ Deux segments (Curator vs Auctioneer)
  ├─ Messages personnalisés (80-100 mots, pas de markdown)
  ├─ Persona Moctar Sidibé
  ├─ Tone chaleureux, direct (pas de vente)
  ├─ Séquence: jour 0 → jour 5-7 follow-up
  ├─ Template email HTML professionnel
  └─ Tracking complet des interactions
```

---

## 🚀 Quick Start (5 minutes)

### **Étape 1: Tester le Service**

```powershell
# Terminal
python test_kucibok_bridge.py

# Output:
# ✅ KUCIBOK BRIDGE OUTREACH SERVICE TEST ✅
# 
# TEST 1: Message Generation by Segment
# TEST 2: Personalization Variants
# TEST 3: Follow-up Message
# TEST 4: HTML Email Rendering
# TEST 5: Rule Validation
#
# ✅ ALL TESTS COMPLETED
```

### **Étape 2: Intégrer avec Deep Source**

```python
# Après avoir trouvé 50 prospects via deep source
from app.db import SessionLocal
from app.services.kucibok_bridge_outreach import KucibokBridgeOutreach

session = SessionLocal()
bridge = KucibokBridgeOutreach(session)

# Pour chaque prospect trouvé
for prospect in prospects:
    # Générer message personnalisé
    message = bridge.generate_message(
        prospect=prospect,
        variant_index=0  # Vary between 0-2 for different messages
    )
    
    # Valider
    rules = bridge.validate_message_rules(message)
    if not any(rules.values()):
        print(f"✅ Message valid for {prospect.name}")
        
        # Logger le message
        bridge.log_outreach(prospect, message, message_type="initial")
    else:
        print(f"❌ Message validation failed: {rules}")

session.close()
```

### **Étape 3: Voir les Résultats**

Accédez au dashboard: **http://localhost:3000**

Vous verrez:
- Tous les prospects par segment
- Messages envoyés (status SENT)
- Réponses reçues
- Taux d'ouverture/clic/réponse

---

## 📋 Règles du Playbook (Non-Négociables)

### **1. Pas de Markdown**

❌ **Mauvais**:
```
Bonjour Marie,

**Voici ce que je propose:**
- Dossier de sourcing
- Artistes vérifiés
- Follow-up personnalisé

Cordialement,
Moctar
```

✅ **Bon**:
```
Bonjour Marie, je vous contacte depuis Dakar où je travaille sur le sourcing d'artistes émergents d'Afrique de l'Ouest pour des curateurs internationaux. Chaque profil est vérifié sur le terrain avant d'être présenté.
```

### **2. 80-100 Mots Maximum**

❌ **Mauvais**: 
```
Bonjour Marie, je suis ravi de vous contacter aujourd'hui depuis Dakar où je consacre mon temps à travailler sur la recherche et le sourcing intensif d'artistes émergents originaires d'Afrique de l'Ouest pour des curateurs internationaux basés en Europe et ailleurs... (trop long!)
```

✅ **Bon**:
```
Bonjour Marie, je vous contacte depuis Dakar où je travaille sur le sourcing d'artistes émergents d'Afrique de l'Ouest pour des curateurs internationaux. Chaque profil est vérifié sur le terrain avant d'être présenté. (52 words)
```

### **3. Toujours Moctar Sidibé**

Le message vient TOUJOURS de Moctar Sidibé, jamais d'un compte "Kucibok" générique.

**Signature à utiliser**:
```
Moctar Sidibé
Kucibok Bridge — Sourcing & Vetting, Dakar
contact@kucibok.com · +221 76 275 09 18
```

### **4. Pas de Mots Interdits**

❌ **Interdits**:
- "IA"
- "Automatisé"
- "Plateforme"
- "Algorithm"

✅ **Remplacés par**:
- "Sourcing basé sur le terrain"
- "Vérification directe"
- "Dossiers complets"

### **5. Une Seule Relance (Si No Response)**

**Séquence**:
- **Jour 0**: Premier message (personnalisé)
- **Jour 5-7**: Relance unique et brève
- **Après**: Arrêter et laisser reposer 2 mois minimum

❌ **Ne pas faire**:
- Deux relances
- Relancer trop tôt (< 5 jours)
- Relancer après silence persistant

### **6. Angle Différent par Segment**

#### **Segment A — Curator/Commissaire d'exposition**

Focus: **Sourcing & dossiers vérifiés**

```
Bonjour [Prénom], votre travail sur [thème précis] rejoint ce que je fais au quotidien à Dakar : sourcer et vérifier des artistes émergents pour des curateurs qui ne peuvent pas se déplacer sur place. Je peux vous envoyer un dossier complet sur un premier profil si vous voulez voir le format.
```

**Angle**: Exposition, démarche curatoriale, réseau international

#### **Segment B — Commissaire-priseur / Maison de vente**

Focus: **Provenance vérifiée, consignation**

```
Bonjour [Prénom], je travaille à Dakar sur la traçabilité et la vérification d'œuvres d'artistes émergents ouest-africains — provenance, disponibilité, documentation complète. Si vos prochains catalogues incluent une section art contemporain africain, je peux vous transmettre un dossier de consignation type.
```

**Angle**: Marché, provenance, documentation, catalogue

---

## 🛠️ Implémentation Technique

### **Service Python**

```python
from app.services.kucibok_bridge_outreach import KucibokBridgeOutreach

bridge = KucibokBridgeOutreach(session)

# Détecter le segment
segment = bridge.detect_segment(prospect)
# → CuratorSegment.CURATOR ou CuratorSegment.AUCTIONEER

# Générer message
message = bridge.generate_message(prospect, variant_index=0)

# Valider
rules = bridge.validate_message_rules(message)
if not any(rules.values()):
    print("✅ Message valid")

# Générer suivi
followup = bridge.generate_followup_message(prospect)

# Rendu HTML
html = bridge.render_html_email(
    prospect=prospect,
    artist_name="Gaétan Rapaccioli",
    artist_city="Dakar",
    artist_country="Senegal",
    artist_medium="Painting",
    works_available=5,
    dossier_url="https://kucibok.com/dossier/gaetan"
)

# Logger
bridge.log_outreach(prospect, message, message_type="initial")
```

### **API Endpoint (À venir)**

```bash
# Générer message pour prospect
POST /api/prospects/{id}/kucibok-bridge-message

Response:
{
    "prospect_id": 1,
    "segment": "CURATOR",
    "message": "Bonjour Marie, je vous contacte...",
    "word_count": 52,
    "validated": true,
    "variants": [
        "Message variant 1...",
        "Message variant 2...",
        "Message variant 3..."
    ]
}
```

---

## 📊 Workflow Complet

```
1. DEEP SOURCE (50 prospects)
   └─ 50 prospects créés (Type: CURATOR)
      └─ Status: IDENTIFIED

2. AUTO-ENRICHMENT (24h)
   └─ Crawl websites
   └─ Extrait emails
   └─ Détecte segment (Curator vs Auctioneer)

3. AUTO-MESSAGE (Kucibok Bridge)
   └─ Générer message personnalisé
   └─ Valider contre les règles
   └─ 45 messages générés (P1-P2)

4. ENVOI MANUEL ou AUTO
   ├─ Option 1: Copier-coller sur LinkedIn
   ├─ Option 2: Envoi via email API
   └─ Moctar Sidibé persona

5. TRACKING (Dashboard)
   └─ Responses reçues?
   └─ Oui → Log as "REPLIED"
   └─ Non → Schedule follow-up day 5-7

6. FOLLOW-UP (Jour 5-7)
   └─ Une seule relance
   └─ Message court et chaleureux

7. RÉSULTATS (30 jours)
   └─ 4-8% taux de réponse
   └─ 2-3 calls planifiés
   └─ 1-2 deals fermés
```

---

## 📧 Template HTML (Inclus)

Le template HTML **Kucibok Bridge** est inclus et contient:

```
Header:
├─ Logo Kucibok Bridge
├─ Bande dorée (#c9a04f)
└─ "Sourcing & Vetting"

Hero Image:
└─ Placeholder pour image artist

Body:
├─ Titre: Nom de l'artiste
├─ Sous-titre: Ville, Pays, Médium
├─ Greeting: "Bonjour [Prénom],"
├─ Main message: Customizable
└─ CTA: "Consulter le dossier complet →"

Info Strip:
├─ Œuvres disponibles
├─ Médium
└─ Statut: "Vérifié"

Signature:
├─ Moctar Sidibé
├─ Kucibok Bridge — Sourcing & Vetting
└─ Contact info

Footer:
├─ Unsubscribe link
└─ Compliance text
```

**Utilisé APRÈS la réponse positive du prospect!**

---

## ✨ Variants de Messages

### **Curator Variant 1** (Standard sourcing pitch)

```
Bonjour [Prénom], je vous contacte depuis Dakar où je travaille sur le sourcing d'artistes émergents d'Afrique de l'Ouest pour des curateurs internationaux. Chaque profil est vérifié sur le terrain avant d'être présenté. Je vous partage volontiers un premier dossier si le sujet vous intéresse, sans engagement.
```

### **Curator Variant 2** (Personalized with context)

```
Bonjour [Prénom], votre travail sur [contexte/expo] rejoint ce que je fais au quotidien à Dakar : sourcer et vérifier des artistes émergents pour des curateurs qui ne peuvent pas se déplacer sur place. Je peux vous envoyer un dossier complet sur un premier profil si vous voulez voir le format.
```

### **Curator Variant 3** (Call-first approach)

```
Bonjour [Prénom], je m'appelle Moctar, basé à Dakar. Je prépare des dossiers de sourcing vérifiés sur des artistes émergents ouest-africains pour des curateurs à l'international. Un appel de 15 minutes vous intéresserait pour voir si ça correspond à vos recherches actuelles ?
```

### **Auctioneer Variant 1** (Provenance & consignment focus)

```
Bonjour [Prénom], je travaille à Dakar sur la traçabilité et la vérification d'œuvres d'artistes émergents ouest-africains — provenance, disponibilité, documentation complète. Si vos prochains catalogues incluent une section art contemporain africain, je peux vous transmettre un dossier de consignation type. Bonne journée.
```

### **Auctioneer Variant 2** (Market opportunity)

```
Bonjour [Prénom], je vous contacte au sujet du marché émergent de l'art contemporain ouest-africain. Je constitue des dossiers de provenance vérifiée sur des artistes encore peu documentés à l'international — utile si vous envisagez d'élargir vos catalogues sur ce segment. Je peux vous envoyer un exemple.
```

---

## 🎯 Checklist Utilisation

### **Avant d'envoyer chaque message**

- [ ] Prospect a un segment assigné (Curator ou Auctioneer)
- [ ] Message est personnalisé (pas copy-paste)
- [ ] Word count: 80-100 words max
- [ ] Pas de markdown
- [ ] Pas de mots interdits (IA, automatisé, plateforme)
- [ ] Signé Moctar Sidibé
- [ ] Statut prospect: IDENTIFIED
- [ ] Excel mise à jour: "À contacter" → "Contacté"

### **Après chaque envoi**

- [ ] Message logué dans database
- [ ] Status mis à jour: "Contacté"
- [ ] Date d'envoi enregistrée
- [ ] Follow-up schedulé (jour 5-7)
- [ ] Dashboard montre le message

### **Si réponse reçue**

- [ ] Status mis à jour: "Répondu"
- [ ] Analyser le message reçu
- [ ] Préparer dossier artist (HTML template)
- [ ] Envoyer dossier + call proposal
- [ ] Log as "REPLIED"

### **Si pas de réponse après 7 jours**

- [ ] Envoyer relance unique
- [ ] Message court: "Je me permets de faire remonter..."
- [ ] Status: "Relancé"
- [ ] Attendre encore 7 jours

### **Après 14 jours sans réponse**

- [ ] Status: "Pas intéressé"
- [ ] Ne pas relancer avant 2 mois minimum
- [ ] Focus sur autres prospects

---

## 📈 Résultats Attendus

```
De 50 prospects trouvés:

✅ Messages générés: 45 (P1-P2 seulement)
✅ Taux de réponse: 8-10% (4-5 réponses)
✅ Taux de call: 4-6% (2-3 appels)
✅ Taux de conversion: 4% (2 deals)
✅ ROI: 50 prospects → €10K-30K revenue
```

---

## 🚀 Prochaines Étapes

1. ✅ Service Python créé (`kucibok_bridge_outreach.py`)
2. ✅ Tests validés (`test_kucibok_bridge.py`)
3. ⏳ Créer API endpoint pour générer messages
4. ⏳ Intégrer avec deep source automation
5. ⏳ Connecter à LinkedIn/email API
6. ⏳ Tracker dans dashboard

---

## 💡 Tips Pro

**Personnalisation efficace**:
- Regarder la colonne "Contexte" dans Excel
- Trouver un détail spécifique (expo, thème, galerie)
- L'utiliser dans le message variant 2

**Timing optimal**:
- Jour 1: Envoi initial (15h-16h)
- Jour 6: Follow-up (11h-12h)

**Tone**:
- Direct, chaleureux
- Pas de commercial appuyé
- Comme un ami qui te recommande

**Segmentation**:
- Curator = focus exposition/démarche
- Auctioneer = focus provenance/marché

---

## 📞 Questions?

Voir les fichiers:
- **Service**: `app/services/kucibok_bridge_outreach.py`
- **Tests**: `test_kucibok_bridge.py`
- **Deep Source**: `DEEP_SOURCE_GUIDE.md`
- **Automation**: `AUTOMATION_COMPLETE.md`
- **Démarrage**: `START_SYSTEM.md`

**Votre système est maintenant complet et prêt pour la prospection professionnelle!** 🚀
