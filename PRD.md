# PRD — Kucibok Prospector V1.1

> **Révision V1.1** — Recentrage du modèle : le payeur du SaaS Kucibok est le **curateur / art advisor**, pas l'artiste. L'artiste est l'actif (le catalogue) qui rend le SaaS désirable, onboardé via Instagram. Cette révision recentre le Prospector sur le **Client Discovery** comme moteur prioritaire, ajoute un module **Outreach Engine** pour les curateurs/advisors, et un module **Artist Onboarding** automatisé via Instagram. Voir sections 6.2, 6.6 et 6.7.

## 1. Contexte

Kucibok construit une infrastructure permettant aux professionnels internationaux de travailler avec le marché de l'art africain depuis leur pays : sourcing d'artistes vérifiés, cotation, logistique Afrique → international, simulation douanière, et tracking de livraison.

Positionnement produit :

> "Kucibok permet aux professionnels internationaux de sourcer des artistes africains vérifiés et de gérer l'opération Afrique → international de bout en bout."

**Le SaaS Kucibok est vendu aux curateurs et art advisors** (galeries internationales et institutions restent des cibles secondaires). Les artistes ne paient pas : ils constituent le catalogue qui rend l'abonnement désirable pour les curateurs/advisors. Cette distinction payeur/actif structure tout le reste du document.

Le Prospector est le premier maillon de cette infrastructure commerciale : il alimente Kucibok en artistes qualifiés (côté offre) et en prospects clients qualifiés et contactés (côté demande, revenu).

## 2. Problème à résoudre

Kucibok n'a aujourd'hui pas de moyen systématique, peu coûteux et évolutif pour :

1. Découvrir des professionnels internationaux (curateurs, art advisors en priorité) susceptibles de payer le SaaS Kucibok, **et les contacter** avec un message pertinent — pas seulement les identifier.
2. Découvrir des artistes africains contemporains pertinents, les documenter, et **les faire rejoindre la plateforme** sans intervention manuelle quotidienne.
3. Prioriser qui contacter, et avec quel message, sur la base de données réelles et non de suppositions.

## 3. Objectif du produit

Construire un agent autonome, auto-hébergé, qui exécute en continu le pipeline :

```
DISCOVER → ENRICH → VERIFY DATA → SCORE → CLASSIFY → STORE → PRIORITIZE
```

sur deux verticales :

- **A. Artist Discovery** → alimente l'**Artist Database**
- **B. Client Discovery** → alimente la **Sales Prospect Database**

Le système doit être conçu dès le départ pour pouvoir être connecté plus tard à la chaîne complète :

```
Prospector → B2B Qualifier → Outreach Writer → SaaS Educator → Meeting Booker → Deal Assistant → Onboarding Agent
```

## 4. Utilisateurs cibles

- **Interne uniquement en V1** : l'équipe Kucibok (fondateur + futurs commerciaux), via le dashboard.
- Pas d'accès externe, pas de self-service client en V1.

## 5. Contrainte produit majeure : coût

Le système ne doit dépendre d'aucun service payant à l'usage pour fonctionner normalement (pas d'API IA facturée à la requête, pas de bases de prospects payantes, pas de scraping payant). Seuls le serveur, le nom de domaine et éventuellement un email professionnel sont des coûts acceptés. Le logiciel lui-même doit être auto-hébergé, open source, et fonctionner avec un modèle IA local.

## 6. Périmètre fonctionnel V1

### 6.1 Client Discovery (moteur prioritaire)

Recherche de professionnels internationaux par ordre de priorité : **art advisors et curateurs en premier** (ce sont les payeurs), puis galeries internationales, puis autres professionnels.

Données collectées : activité professionnelle, pays, ville, activité internationale, intérêt pour l'art africain, intérêt pour les scènes émergentes, activité de sourcing, artistes représentés si connu, expositions, foires, clientèle si publiquement identifiable, maturité digitale, signaux récents.

Sortie : **SaaS Fit Score** (/100), **Confidence Score**, **Priority** (P1–P4), **Reason to Contact**, **Recommended Angle**.

### 6.2 Artist Discovery (moteur de soutien)

Recherche des artistes africains contemporains (émergents ou confirmés) ayant une activité professionnelle documentable : portfolio, expositions, résidences, foires, galeries, prix. Objectif V1 : suffisant pour rendre le catalogue crédible auprès des premiers curateurs/advisors payants — pas exhaustif.

Données collectées : nom, pays, ville, origine/nationalité si publiquement déclarée, discipline, médium, style, biographie, site, Instagram public, LinkedIn public si pertinent, galerie, expositions, résidences, foires, prix/distinctions, portfolio, œuvres publiques, sources.

Sortie : **Artist Fit Score** (/100) + statut (`IDENTIFIED` → `PREQUALIFIED` max en automatique).

### 6.3 Détection de signaux d'intention

Le système détecte des événements publics récents indiquant un besoin potentiel (nouvelle exposition Afrique, appel à artistes, participation à une foire africaine, nouveau programme international, etc.), chacun caractérisé par : type, description, source, date, importance (LOW/MEDIUM/HIGH), confiance.

### 6.4 Dashboard

Vue d'ensemble (compteurs par type/statut/priorité), liste filtrable, fiche prospect détaillée, export CSV/JSON.

### 6.5 Automatisation

Exécution quotidienne planifiée du pipeline complet (discovery → crawling → enrichissement → analyse IA → scoring → mise à jour base), avec file de jobs, retries (max 3), et monitoring.

### 6.6 Outreach Engine (nouveau — cible : curateurs / art advisors)

Génère automatiquement, sans validation humaine, les messages de contact pour les prospects Client Discovery priorisés (P1 → P4). Détecte la persona (Art Advisor / Curator), produit plusieurs variantes courtes basées sur le Reason to Contact et le Recommended Angle, sans mise en forme markdown (format déjà validé par Khalif). Si la confiance sur un prospect est LOW, le message reste générique mais pertinent — jamais de détail inventé (garde-fou renforcé, voir section 7).

**L'envoi reste manuel, sur LinkedIn, effectué par Khalif** : le système ne se connecte à aucun compte LinkedIn et n'automatise aucun envoi — zéro automatisation d'envoi LinkedIn (risque de bannissement de compte contraire aux CGU LinkedIn). Le dashboard présente une file d'envoi triée par priorité, prête à copier-coller, avec suivi manuel de statut (`SENT`) et d'issue (`REPLIED` / `MEETING` / `CUSTOMER` / `LOST` / `NOT_RELEVANT`).

### 6.7 Artist Onboarding via Instagram (nouveau — automatisé, sans validation)

Pipeline entièrement automatisé, du repérage à l'inscription sur la plateforme, **sans validation manuelle de Khalif**, avec une contrainte de conformité stricte :

1. Découverte + scoring + pré-remplissage du profil artiste : automatique (réutilise l'Artist Discovery).
2. Génération du message d'invitation à rejoindre Kucibok : automatique.
3. **Envoi du message et création de compte : déclenchés uniquement après un premier contact initié par l'artiste lui-même** (clic sur lien en bio, réponse à story, formulaire), via l'API officielle Instagram Business Messaging. Aucun DM à froid non sollicité envoyé par bot — l'API Meta ne le permet pas légitimement, et le contournement expose le compte Instagram professionnel de Kucibok à un bannissement.
4. Une fois le contact initié, relance et complétion du profil jusqu'à l'inscription peuvent être automatisées sans intervention humaine.

Ce compromis respecte la demande de zéro effort manuel quotidien tout en évitant un risque de bannissement du canal marketing Instagram de Kucibok et le risque réputationnel d'un profil artiste créé/inscrit automatiquement sans confirmation de l'intéressé.

## 7. Garde-fous produit (non négociables)

- Le Prospector **ne déclare jamais** un artiste "Vérifié Kucibok" — seul un humain ou un futur agent de vérification dédié peut le faire.
- Aucune information n'est inventée : si une donnée est absente, elle est marquée `UNKNOWN`. Chaque affirmation importante doit être reliée à une source enregistrée.
- Le Prospector ne réalise **aucune** action des agents suivants au-delà de la génération de message (qualification approfondie, prise de rendez-vous). Il livre des leads structurés, qualifiés, et des messages prêts à envoyer.
- Aucun contournement de login, CAPTCHA, paywall ou protection technique. Accès aux données publiques uniquement, dans le respect de robots.txt et des limites de fréquence.
- **Aucune automatisation d'envoi sur LinkedIn.** Le système génère, ne se connecte jamais à un compte LinkedIn.
- **Aucun DM Instagram à froid envoyé par bot.** Tout envoi automatisé côté artiste passe par l'API officielle Instagram Business et suppose un contact initié par l'artiste.
- Aucune création de compte/profil artiste public sans un premier contact confirmé de l'intéressé.

## 8. Métriques de succès (KPI MVP)

| Métrique | Cible |
|---|---|
| Artistes identifiés | ≥ 100 / mois |
| Prospects clients identifiés | ≥ 100 / mois |
| Prospects avec au moins une source exploitable | > 90 % |
| Prospects jugés pertinents lors de validation humaine | > 70 % |
| Taux de doublons | < 5 % |
| Disponibilité du système | > 95 % |

## 9. Hors périmètre V1

- Vérification officielle des artistes (reste humaine)
- Envoi automatisé de messages sur LinkedIn (génération oui, envoi non)
- DM Instagram à froid non sollicité
- Prise de rendez-vous automatisée
- Auto-apprentissage / auto-modification du scoring (les règles restent modifiables manuellement uniquement)
- Interface client externe / self-service

## 10. Definition of Done

Voir la checklist complète dans `/docs/ROADMAP.md`, section Definition of Done.
