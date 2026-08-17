# LOGIC — Kucibok Prospector V1.1

> **Révision V1.1** : Client Discovery (curateurs/advisors) est le pipeline prioritaire — c'est le payeur. L'Artist Discovery alimente désormais un onboarding automatisé via Instagram (section 17). Un nouveau pipeline Outreach Engine (section 16) génère les messages de contact pour les curateurs/advisors.

Ce document décrit la logique métier du système : pipelines, scoring, garde-fous IA et modèle de données. C'est la référence pour comprendre "pourquoi le système décide ce qu'il décide".

## 1. Principe général : séparer données et jugement

```
RAW DATA → FEATURE EXTRACTION → RULE ENGINE → SCORE → LLM INTERPRETATION
```

Le LLM ne pilote jamais seul la décision commerciale. Le scoring est calculé par un moteur de règles explicable et testable ; le LLM intervient pour l'analyse qualitative (résumé, détection de signaux, rédaction du "Reason to Contact", identification des données manquantes, recommandation d'angle) — jamais pour calculer le score final seul.

## 2. Pipeline Artiste

```
DISCOVERY → IDENTITY → DEDUPLICATION → WEBSITE/PROFILE → CRAWLING
→ EXTRACTION → ENRICHMENT → ARTIST ANALYSIS → ARTIST FIT SCORE
→ CONFIDENCE → PREQUALIFIED → DATABASE
```

## 3. Pipeline Client

```
DISCOVERY → IDENTITY → DEDUPLICATION → WEBSITE/PROFILE → CRAWLING
→ EXTRACTION → ENRICHMENT → AFRICA INTEREST → OPERATIONAL NEED
→ INTENT SIGNALS → SAAS FIT SCORE → CONFIDENCE → PRIORITY → DATABASE
```

## 4. Artist Fit Score (/100)

| Composante | Points |
|---|---|
| Qualité du profil | 20 |
| Potentiel international | 20 |
| Présence professionnelle/digitale | 15 |
| Potentiel commercial | 20 |
| Documentation des œuvres | 15 |
| Compatibilité Kucibok | 10 |

Classification :

- **80–100 : PRIORITY**
- **65–79 : PROMISING**
- **50–64 : WATCHLIST**
- **0–49 : LOW PRIORITY**

Le score doit toujours être restitué avec son détail, par exemple :

```
Artist Fit Score : 87
Breakdown :
  Profile Quality        18/20
  International Potential 17/20
  Digital Presence        13/15
  Commercial Potential    18/20
  Documentation           12/15
  Kucibok Fit              9/10
```

## 5. Statuts artiste

```
IDENTIFIED → PREQUALIFIED → DOCUMENTATION_REQUESTED → VERIFICATION_IN_PROGRESS → VERIFIED_KUCIBOK
```

**Règle stricte : le Prospector ne peut jamais attribuer automatiquement `VERIFIED_KUCIBOK`. Le statut automatique maximal est `PREQUALIFIED`.**

## 6. SaaS Fit Score (/100)

| Composante | Points |
|---|---|
| Besoin potentiel de sourcing africain | 30 |
| Besoin opérationnel | 20 |
| Activité internationale | 15 |
| Capacité commerciale estimée | 15 |
| Maturité digitale | 10 |
| Signal d'intention | 10 |

Classification :

- **80–100 : HOT**
- **65–79 : WARM**
- **50–64 : WATCHLIST**
- **0–49 : LOW**

## 7. Confidence Score

Score indépendant : **LOW / MEDIUM / HIGH**, basé sur la quantité et la qualité des sources disponibles.

Un score élevé avec une confiance faible ne doit **jamais** être traité comme un lead fiable. Exemple : `SaaS Fit Score = 90`, `Confidence = LOW` signifie "le prospect semble très intéressant mais les données disponibles sont insuffisantes" — il ne doit pas être promu en HOT tant que les données manquent.

## 8. Priority Score (P1–P4)

Calculée à partir de : score, confidence, récence des signaux, qualité des données.

- **P1** : contact immédiat
- **P2** : contact cette semaine
- **P3** : nurturing / watchlist
- **P4** : archive

## 9. Signaux d'intention (Intent Signals)

Événements publics récents indiquant un besoin potentiel (nouvelle exposition Afrique, recherche d'artistes africains, participation à une foire africaine, appel à artistes, ouverture d'implantation, publication récente concernant l'Afrique, etc.).

Chaque signal comporte : `signal_type`, `description`, `source_url`, `signal_date`, `importance` (LOW/MEDIUM/HIGH), `confidence`.

## 10. Reason to Contact

Pour chaque prospect qualifié, générer trois blocs, strictement basés sur des données trouvées (aucune invention) :

- **WHY** — pourquoi ce prospect correspond à Kucibok
- **WHY NOW** — pourquoi le contacter maintenant
- **WHAT** — quelle proposition Kucibok est la plus pertinente

## 11. Recommended Angle

Un angle est choisi parmi : `SOURCING`, `LOGISTICS`, `SOURCING_AND_LOGISTICS`, `DISCOVERY`, `INTERNATIONAL_ACCESS`.

Exemples :
- Art advisor intéressé par l'Afrique mais peu de contenu logistique → `SOURCING`
- Galerie ayant déjà travaillé avec des artistes africains mais avec des difficultés opérationnelles → `LOGISTICS`
- Galerie voulant développer son activité Afrique de zéro → `SOURCING_AND_LOGISTICS`

## 12. Déduplication

Détection des doublons par ordre de priorité : domaine → email → LinkedIn → Instagram → nom normalisé + pays.

- Doublon détecté → `UPDATE` du prospect existant
- Sinon → `CREATE`

Normalisation systématique : noms, pays, villes, URLs, catégories, réseaux sociaux.

## 13. Analyse IA — structure stricte

Le modèle local retourne toujours une structure JSON stricte, jamais du texte libre pour les données critiques :

```json
{
  "classification": "",
  "score": 0,
  "confidence": "",
  "reason": "",
  "africa_interest": "",
  "operational_need": "",
  "intent_signals": [],
  "recommended_angle": "",
  "missing_data": []
}
```

## 14. Garde-fous IA (non négociables)

Le modèle doit utiliser `UNKNOWN` lorsqu'une information est absente. Il ne doit **jamais** :

- inventer un email, un site, une exposition ;
- inventer une relation avec l'Afrique, une vente, une clientèle ;
- déclarer une vérification Kucibok ;
- transformer une hypothèse en fait.

Toute information importante doit pouvoir être reliée à une source enregistrée (table `sources`).

## 15. Crawler — règles de conduite

Le crawler télécharge des pages publiques, extrait texte et liens, identifie les pages About/Team/Artists/Exhibitions/Contact, détecte réseaux sociaux et emails publics. Il respecte robots.txt et les limites de fréquence, et n'accède qu'à du contenu public. Il ne contourne jamais login, CAPTCHA, paywall ou protection technique.

## 16. Outreach Engine (curateurs / art advisors)

### 16.1 Déclenchement

Un prospect entre dans l'Outreach Engine dès qu'il a un `SaaS Fit Score`, une `Confidence`, et une `Priority` calculés (fin du pipeline Client Discovery, section 3). Aucune validation humaine n'intervient dans la génération.

### 16.2 Génération de message

```
Prospect (persona: ART_ADVISOR | CURATOR)
  + Reason to Contact (WHY / WHY NOW / WHAT)
  + Recommended Angle
  + Confidence
        ↓
   Message Generator (AIProvider)
        ↓
   Plusieurs variantes courtes, sans markdown, ton direct
```

Règles :

- Format aligné sur le style déjà validé par Khalif : messages courts, sans formatage markdown, plusieurs longueurs par persona.
- Si `Confidence = LOW` : le message reste générique et pertinent au niveau du persona/secteur, mais **ne mentionne aucun détail spécifique non confirmé par une source** (pas de fausse exposition citée, pas de fausse activité Afrique inventée). C'est le dernier filet de sécurité puisqu'il n'y a plus de relecture humaine avant copier-coller — la règle "aucune invention" (section 14) s'applique ici avec une exigence renforcée.
- Chaque message généré est stocké, jamais modifié rétroactivement — une nouvelle génération crée une nouvelle ligne.

### 16.3 File d'envoi

Le dashboard présente les messages triés par `Priority` (P1 → P4), avec le lien LinkedIn du prospect et le(s) message(s) prêts à copier. Khalif envoie manuellement sur LinkedIn — **le système ne se connecte à aucun compte LinkedIn et n'automatise aucun envoi**, pour éviter tout risque de bannissement de compte (contraire aux CGU LinkedIn).

### 16.4 Suivi

Statut du message : `DRAFT` → `SENT` (marqué manuellement par Khalif après envoi). Issue du contact, saisie manuellement au fil de l'eau : `REPLIED`, `MEETING`, `CUSTOMER`, `LOST`, `NOT_RELEVANT`. Alimente la couche feedback future (section 18), sans auto-apprentissage en V1.

## 17. Artist Onboarding via Instagram

### 17.1 Contrainte de conformité

L'API officielle Instagram Business Messaging ne permet pas d'initier un contact avec un compte qui n'a jamais interagi avec Kucibok — elle sert à répondre à des conversations déjà ouvertes par l'utilisateur. Tout DM à froid automatisé nécessiterait un contournement non-officiel, ce qui expose le compte Instagram professionnel de Kucibok à un bannissement. **Cette contrainte n'est pas négociable et détermine tout le pipeline ci-dessous.**

### 17.2 Pipeline

```
ARTIST DISCOVERY (existant, section 2)
        ↓
   Pré-remplissage du profil (nom, pays, discipline, médium, portfolio, sources)
        ↓
   Génération du message d'invitation (automatique)
        ↓
   [ATTENTE] Premier contact initié par l'artiste
     (clic lien en bio / réponse story / formulaire public)
        ↓
   Envoi automatisé via API Instagram Business Messaging
   (autorisé : la conversation est ouverte par l'artiste)
        ↓
   Relance + complétion automatique du profil
        ↓
   Inscription sur la plateforme (automatique, sans validation humaine)
```

### 17.3 Ce qui est automatique de bout en bout, sans validation de Khalif

- Découverte, scoring, pré-remplissage
- Génération du message d'invitation
- Envoi, relance et complétion **une fois le contact initié par l'artiste**
- Création finale du compte/inscription

### 17.4 Ce qui reste exclu, même en automatisation totale

- Aucun DM à froid non sollicité
- Aucune création de profil/compte public tant que l'artiste n'a pas lui-même initié le contact — un profil pré-rempli à partir de données scrapées reste en `IDENTIFIED`/`PREQUALIFIED` interne, invisible publiquement, tant qu'il n'y a pas eu de confirmation de l'intéressé.

## 18. Feedback futur (V2+)

Chaque prospect conserve son historique : score initial, segment, pays, angle, statut, et un futur `outcome` (`REPLIED`, `MEETING`, `CUSTOMER`, `LOST`, `NOT_RELEVANT`) qui alimentera plus tard une couche d'apprentissage. **En V1, aucune auto-modification du scoring** : les règles restent modifiables manuellement uniquement.
