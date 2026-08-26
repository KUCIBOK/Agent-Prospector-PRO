# 🚀 ROADMAP - APRÈS LA PROSPECTION

**Vous avez:** 75 prospects réalistes à Paris  
**Objectif:** Convertir en clients payants  
**Durée:** 30 jours  
**ROI attendu:** 2-3 deals fermés

---

## 📋 PHASES DE LA CONVERSION

```
PHASE 1: ENRICHISSEMENT (Jour 1-2)
    ↓
PHASE 2: SCORING & SEGMENTATION (Jour 2-3)
    ↓
PHASE 3: PERSONNALISATION (Jour 3-4)
    ↓
PHASE 4: OUTREACH (Jour 5-7)
    ↓
PHASE 5: FOLLOW-UPS (Jour 8-30)
    ↓
PHASE 6: CONVERSION (Jour 15-30)
```

---

## 🔧 **PHASE 1: ENRICHISSEMENT DES DONNÉES (Jour 1-2)**

### **Objectif**
Compléter les profils des prospects avec des informations détaillées

### **Actions**

**1.1 Scraper les websites**
```python
For each prospect:
  ├─ Accéder au website
  ├─ Extraire: type de galerie, artistes représentés, expositions
  ├─ Déterminer: spécialité, style, budget apparent
  └─ Mettre à jour la base de données
```

**Outil:** Web scraper (BeautifulSoup, Selenium)  
**Temps:** ~2 secondes par prospect = 2-3 minutes pour 75  
**Résultat:** Profils 80% complets

**1.2 Scraper les réseaux sociaux**
```python
For each prospect:
  ├─ LinkedIn: Parcours professionnel, changements récents
  ├─ Instagram: Style, engagement, followers
  └─ Twitter/Facebook: Activité récente, intérêts
```

**Outil:** API LinkedIn (si access), Instagram scraper  
**Temps:** ~5 secondes par prospect = 6-7 minutes  
**Résultat:** Signaux d'intention détectés

**1.3 Compléter les contacts**
```python
For each prospect:
  ├─ Chercher email personnel (pas juste domaine)
  ├─ Chercher téléphone si disponible
  ├─ Chercher directeur/PDG/curator principal
  └─ Valider les emails (Hunter.io, Clearbit)
```

**Outil:** Hunter.io API, Clearbit API  
**Temps:** ~1 seconde par prospect = 1-2 minutes  
**Résultat:** Emails 90% validés

### **Résultat Attendu**
```
75 prospects avec:
  ✅ Website info complet
  ✅ Social media data
  ✅ Emails validés
  ✅ Contacts principaux identifiés
  ✅ Specialité confirmée
```

---

## ⭐ **PHASE 2: SCORING & SEGMENTATION (Jour 2-3)**

### **Objectif**
Évaluer le potentiel de chaque prospect et les segmenter

### **2.1 Scoring Advanced Artist**

**Fair Score (0-100)** - Potentiel artistique
```
Critères:
  ├─ Qualité de la collection (photos, descriptions)
  ├─ Nombre d'artistes représentés
  ├─ Historique de ventes apparent
  ├─ Engagement client (réseaux sociaux)
  └─ Réputation (avis, critiques)

Formule:
  Fair Score = (Quality × 0.3) + (Volume × 0.2) + (Engagement × 0.3) + (Reputation × 0.2)
```

**Gallery Score (0-100)** - Visibilité & infrastructure
```
Critères:
  ├─ Taille de la galerie (m²)
  ├─ Localisation (prestige de la rue)
  ├─ Online presence (website, Instagram followers)
  ├─ Volume d'expositions par an
  └─ Types d'expositions (solo, collections, etc)

Formule:
  Gallery Score = (Size × 0.2) + (Location × 0.2) + (Online × 0.3) + (Activity × 0.3)
```

**Awards Score (0-100)** - Reconnaissances
```
Critères:
  ├─ Prix/Awards reçus
  ├─ Mentions dans presse spécialisée
  ├─ Collaborations prestigieuses
  ├─ Participation foires internationales
  └─ Certifications (UNESCO, labels, etc)

Formule:
  Awards Score = (Prizes × 0.4) + (Press × 0.3) + (Collab × 0.2) + (Intl × 0.1)
```

**Final Score**
```
Final Score = (Fair × 0.35) + (Gallery × 0.35) + (Awards × 0.30)
Range: 0-100

Interprétation:
  80-100: EXCELLENT (Top prospects)
  60-79: BON (Bons prospects)
  40-59: MOYEN (À nurture)
  0-39: FAIBLE (Long-term nurturing)
```

### **2.2 Re-Prioritization**

```
P1 (Contacter immédiatement) = Final Score ≥ 75
P2 (Cette semaine) = Final Score 60-74
P3 (Nurturing) = Final Score 40-59
P4 (Archive) = Final Score < 40
```

**Avant Scoring:**
```
P1: 15 prospects
P2: 18 prospects
P3: 42 prospects
```

**Après Scoring Avancé:**
```
P1: 25-30 prospects (TOP HOT)
P2: 25-30 prospects
P3: 15-20 prospects
P4: 0-5 prospects
```

### **2.3 Segmentation**

**Par Type de Client:**
```
Segment A: Galeries Internationales
  └─ Focus: Partenariat long-terme, distribution
  
Segment B: Galeries Parisiennes Prestige
  └─ Focus: Exhibitions, collaborations
  
Segment C: Art Advisors/Curators
  └─ Focus: Sourcing services, consulting
  
Segment D: Collectors/Institutions
  └─ Focus: Acquisitions, collections
```

**Par Maturité:**
```
Segment 1: Ready to Buy (Score 80+)
  └─ Action: Direct sales outreach
  
Segment 2: Interested (Score 60-79)
  └─ Action: Educational content + nurturing
  
Segment 3: Long-term (Score 40-59)
  └─ Action: Regular newsletter + engagement
  
Segment 4: Maybe (Score < 40)
  └─ Action: Quarterly check-in
```

### **Résultat Attendu**
```
75 prospects avec:
  ✅ Fair Score (0-100)
  ✅ Gallery Score (0-100)
  ✅ Awards Score (0-100)
  ✅ Final Score (0-100)
  ✅ Nouvelle priorité (P1-P4)
  ✅ Segment assigné
  ✅ Stratégie définie
```

---

## 📝 **PHASE 3: PERSONNALISATION DES MESSAGES (Jour 3-4)**

### **Objectif**
Créer des emails personnalisés pour chaque prospect

### **3.1 Analyse du Prospect**

Pour chaque prospect, créer un profil détaillé:
```
{
  "name": "Marie Dubois",
  "gallery_name": "Galerie d'Art Contemporain",
  "type": "CURATOR",
  "speciality": "African Contemporary Art",
  "recent_exhibitions": ["Afro-Modernism", "Future Africa"],
  "key_artists": ["Artist A", "Artist B"],
  "engagement_level": "HIGH",
  "final_score": 87,
  "segment": "A - International Gallery",
  "angle": "Partnership + Distribution"
}
```

### **3.2 Personnaliser les Messages**

**Template Par Segment:**

**Segment A: Partnership (Score 80+)**
```
Subject: Partnership Opportunity - African Contemporary Artists

Body:
Dear [Name],

I noticed your recent exhibition on [Exhibition Name] at [Gallery].
Your work with [Artist Names] aligns perfectly with our mission to connect
African artists with international platforms.

We represent [Number] emerging artists and have successfully placed works
in galleries similar to yours. I believe there's strong potential for partnership.

Would you be interested in a brief call (15 min) to explore collaboration opportunities?

Best regards,
[Your Name]
```

**Segment B: Consultation (Score 60-79)**
```
Subject: Curating African Contemporary - Free Insights

Dear [Name],

As a curator specializing in [Speciality], you might find this valuable:
[Useful resource about African art trends, market insights]

I'd love to share more insights about emerging African artists
and trends you might not have discovered yet.

Can we schedule a quick call?

Best,
[Your Name]
```

**Segment C: Newsletter (Score 40-59)**
```
[Monthly newsletter with artist features, exhibitions, market trends]

No pressure - just valuable content for art professionals like you.
```

### **3.3 Stratégies de Personnalisation**

**Par Type de Galerie:**
```
Luxury Gallery → Focus: Exclusivity, Premium positioning
Regional Gallery → Focus: Expansion, New markets
Online Gallery → Focus: Digital innovation, Global reach
Museum/Institution → Focus: Educational, Curatorial excellence
```

**Par Géographie:**
```
Paris (Prime Location) → Focus: Already sophisticated, Partnership angle
Paris (Secondary) → Focus: Growth opportunity, Visibility
```

**Par Engagement Level:**
```
High Engagement → Direct outreach, Personal phone call
Medium Engagement → Email + follow-up
Low Engagement → Newsletter + retargeting later
```

### **Résultat Attendu**
```
75 prospects avec:
  ✅ Profil personnalisé
  ✅ Angle de vente défini
  ✅ Message personnalisé
  ✅ Subject line optimisé
  ✅ Call-to-action clair
  ✅ Timeline de suivi prévu
```

---

## 📧 **PHASE 4: OUTREACH (Jour 5-7)**

### **Objectif**
Envoyer les messages personnalisés et générer des réponses

### **Stratégie d'Envoi**

**P1 Prospects (25-30) - Hot Outreach:**
```
Jour 5-6: Envoi email initial
├─ Subject: Personnalisé, avec hook spécifique
├─ Body: 150-200 mots, focaliser sur LEUR problème
├─ CTA: Clair (Call/Meeting request)
└─ Signature: Professional avec links

Envoi timing: 
  └─ Mardi-Jeudi 9:00-11:00 AM (meilleur taux d'ouverture)
  └─ Décalé par fuseaux horaires si pertinent

Suivi timing:
  └─ Follow-up 1: +3 jours si pas de réponse
  └─ Follow-up 2: +7 jours si pas de réponse
```

**P2 Prospects (25-30) - Nurture Outreach:**
```
Jour 6-7: Envoi email éducatif
├─ Subject: Value-focused (insights, trends, resources)
├─ Body: Contenu utile + subtle pitch
├─ CTA: Soft (Subscribe / Learn more)
└─ Timing: Plus flexible

Suivi:
  └─ Newsletter mensuelle
  └─ Retargeting email si engagement détecté
```

### **4.1 Email Template Optimisé**

**Structure (Proven High-Conversion):**
```
1. SUBJECT LINE (7-10 words, personalized)
   └─ Example: "African Contemporary Art - Opportunity for [Gallery Name]"
   └─ Goal: 40%+ open rate

2. GREETING (Personal)
   └─ "Dear Marie,"
   └─ Not "Hello everyone"

3. HOOK (First 2 lines - WHY THEY SHOULD READ)
   └─ Reference something specific about THEM
   └─ Example: "I saw your recent exhibition on [Topic]"

4. VALUE STATEMENT (What's in it for them)
   └─ 3-4 sentences explaining benefit
   └─ NOT about you, about THEM

5. PROOF/SOCIAL PROOF (Why you can deliver)
   └─ "We've successfully worked with [Gallery Names]"
   └─ Numbers: "50+ artists represented"

6. CTA (Crystal clear)
   └─ "Can we schedule 15 minutes this week?"
   └─ Provide 3 time slots
   └─ Make it EASY to say yes

7. SIGNATURE (Professional)
   └─ Name, Title, Contact, Company Info
```

### **Résultat Attendu**
```
Jour 7-10:
  ├─ 75 emails envoyés
  ├─ ~30-40% ouverture attendue (25-30 opens)
  ├─ ~5-8% click-through (4-6 clicks)
  ├─ ~2-4% réponses initiales (2-3 réponses)
  └─ 10-15 prospects qualifiés pour conversation
```

---

## 🔄 **PHASE 5: FOLLOW-UPS & NURTURING (Jour 8-30)**

### **Jour 8-10: Premier Follow-up (Si pas de réponse)**

```python
For each P1 prospect without response:
  ├─ Send follow-up email
  ├─ Subject: Re: [Original Subject] - Quick thought
  ├─ Body: Shorter, new angle, social proof
  ├─ CTA: Same (but more urgent - "This week")
  └─ Note: 40-50% de réponses supplémentaires
```

### **Jour 15-20: Deuxième Follow-up**

```python
For each prospect still no response:
  ├─ Change channel: Try phone call if you have number
  ├─ Or: Send different content (case study, article)
  ├─ Body: "Noticed you haven't replied - too busy? I get it."
  ├─ CTA: Lower pressure ("Just let me know if interested")
  └─ Note: 20-30% de nouvelles réponses
```

### **Jour 25-30: Final Follow-up**

```python
For prospects with no response:
  ├─ Accept: They're not interested NOW
  ├─ Add to: Quarterly nurture email list
  ├─ Send: "We'll check in quarterly with updates"
  ├─ CTA: Soft ("No pressure, but here's what's new")
  └─ Note: 5-10% reply later months
```

### **Nurture Track (Parallel)**

```
For Interested but Not Ready (P2-P3):
  ├─ Weekly newsletter with:
  │  ├─ Artist features
  │  ├─ Market insights
  │  ├─ Exhibition announcements
  │  └─ Success stories
  │
  ├─ Monthly webinars:
  │  ├─ "African Contemporary Market Trends"
  │  ├─ "How to Source Emerging Artists"
  │  └─ "Gallery Partnerships Strategy"
  │
  └─ Triggered emails:
     ├─ If they click link → Educational content
     ├─ If they open email → Next segment offer
     └─ After 30 days → Personal outreach
```

### **Résultat Attendu - Jour 30**

```
De 75 prospects:
  ├─ 15-20 CONVERSATIONS QUALIFIÉES (20-27%)
  │  └─ Soit: Phone/Zoom call scheduled
  │
  ├─ 30-40 NURTURING TRACK (40-53%)
  │  └─ Soit: Interested but needs more time
  │
  ├─ 15-25 NOT INTERESTED (20-33%)
  │  └─ Soit: Rejected or ghosted
  │
  └─ 2-3 DEALS FERMÉS (2-4%)
     └─ Soit: Contrats signés!
```

---

## 💰 **PHASE 6: CONVERSION (Jour 15-30)**

### **Pour les 15-20 Conversations Qualifiées**

**Étape 1: Call/Meeting (Jour 8-15)**
```
Objectifs:
  ├─ Qualifier: Sont-ils vraiment intéressés?
  ├─ Pain Points: Quels sont leurs besoins?
  ├─ Budget: Ont-ils un budget?
  ├─ Timeline: Quand veulent-ils décider?
  └─ Decision Maker: Parlez-vous au bon décideur?

Script 15 minutes:
  1. Ouverture chaleureuse (1 min)
  2. Rapport sur leur galerie (2 min)
  3. Poser questions sur besoins (5 min)
  4. Présenter votre value prop (4 min)
  5. Próximos pasos (3 min)
```

**Étape 2: Proposal (Jour 16-20)**
```
Si intéressé + Qualified:
  ├─ Envoyer proposal personnalisée
  ├─ Inclure:
  │  ├─ Comprendre leurs besoins
  │  ├─ Votre solution spécifique
  │  ├─ Pricing (3 options: Basic/Standard/Premium)
  │  ├─ Timeline (30-60-90 jours)
  │  ├─ Témoignages clients similaires
  │  └─ Next steps clairs
  │
  └─ Attendre réponse (3-5 jours)
```

**Étape 3: Negotiation (Jour 20-25)**
```
Si questions sur proposal:
  ├─ Quick call pour clarifier
  ├─ Adresser objections:
  │  ├─ "Trop cher?" → ROI analysis
  │  ├─ "Pas certain?" → Free pilot/trial
  │  ├─ "Pas now?" → Lock-in 3-mois à discount
  │  └─ "Besoin d'approuver?" → Present to decision-makers
  │
  └─ Close when ready
```

**Étape 4: Signature & Onboarding (Jour 25-30)**
```
Si accord:
  ├─ Envoyer contrat
  ├─ Onboarding call
  ├─ Setup initial (données, access, etc)
  ├─ Démarrer service
  └─ Schedule review dans 30 jours
```

### **Taux de Conversion Attendus**

```
De 75 prospects initiaux:
  └─ 30-40 qualified conversations (40-53%)
     └─ 15-20 proposals envoyées (50% de conversations)
        └─ 8-12 objections surmontées (50-60% de proposals)
           └─ 2-3 DEALS FERMÉS (20-30% de propositions)
              
RÉSULTAT FINAL: 2-3 DEALS FERMÉS = 2.7-4% CONVERSION RATE
```

---

## 📊 **TIMELINE COMPLÈTE - 30 JOURS**

```
JOUR 1-2:   Enrichissement données (Websites, Social, Emails)
JOUR 2-3:   Scoring & Segmentation (Fair/Gallery/Awards)
JOUR 3-4:   Personnalisation messages
JOUR 5-6:   Envoi P1 outreach
JOUR 6-7:   Envoi P2 nurturing
JOUR 8-10:  Première round de follow-ups
JOUR 10-15: Calls/meetings avec intéressés
JOUR 15-20: Deuxième wave de follow-ups
JOUR 16-20: Proposals pour qualified leads
JOUR 20-25: Negotiation & objection handling
JOUR 25-30: Closing & onboarding
JOUR 30:    Première review & renewal planning
```

---

## 🎯 **RÉSULTATS ATTENDUS**

```
Jour 30 Targets:

Conversations:  15-20 qualifiées (20-27% of 75)
Proposals:      8-12 envoyées (50-60% of conversations)
Deals:          2-3 fermés (2.7-4% of 75)

Revenue:
  └─ Par deal: €5,000-15,000 (depending on service)
  └─ Total: €10,000-45,000 (2-3 deals × €5k-15k)
  
ROI:
  └─ Cost per prospect: ~€50-100 (if outsourced)
  └─ CAC (Customer Acquisition Cost): ~€2,000-5,000
  └─ LTV (Lifetime Value): €20,000-100,000
  └─ ROI: 400-2000% over 12 months
```

---

## 🚀 **NEXT STEPS IMMÉDIATS**

```
DEMAIN (Jour 1):
  [ ] Enrichir 10 premiers prospects (test)
  [ ] Valider la qualité enrichissement
  [ ] Ajuster script si besoin
  
JOUR 2:
  [ ] Enrichir les 65 restants
  [ ] Vérifier emails validés
  [ ] Commencer scoring
  
JOUR 3:
  [ ] Finir scoring avancé
  [ ] Segmenter prospects
  [ ] Écrire 5 email templates
  
JOUR 4:
  [ ] Personnaliser messages pour P1
  [ ] Tester avec 3-5 prospects
  [ ] Ajuster subject line + body
  
JOUR 5-6:
  [ ] LANCER OUTREACH P1 (25-30 emails)
  [ ] Monitorer opens, clicks, replies
  [ ] Être prêt pour appels
```

---

## 📞 **POUR ALLER PLUS LOIN**

**Outils recommandés:**

```
Enrichissement:
  • Hunter.io (emails validation)
  • Clearbit (company data)
  • RocketReach (personal emails)

Outreach:
  • Mailchimp (emails à petite scale)
  • Outreach.io (sophisticated outreach)
  • Lemlist (personalization at scale)

Tracking:
  • HubSpot (free CRM)
  • Pipedrive (sales pipeline)
  • Close.io (sales automation)

Meeting scheduling:
  • Calendly (free scheduling)
  • Outreach.io (built-in)
```

---

**Vous êtes maintenant prêt à convertir 75 prospects en 2-3 deals payants en 30 jours! 🚀**

Questions? Besoin d'aide sur l'une des phases?
