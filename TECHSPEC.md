# TECHSPEC — Kucibok Prospector V1.1

> **Révision V1.1** : ajout du module Outreach Engine (curateurs/advisors, génération seule, pas de connexion LinkedIn) et du module Artist Onboarding Instagram (envoi conditionné à un contact initié par l'artiste, via API officielle uniquement).

## 1. Principes d'architecture

- Monolithe modulaire, dockerisé — pas de microservices, pas de Kubernetes, pas d'architecture distribuée.
- Priorité : fiabilité + simplicité + coût minimal + évolutivité.
- Aucune dépendance runtime payante à l'usage.
- Modulaire dès le départ pour permettre le branchement futur d'agents supplémentaires (Qualifier, Outreach Writer, etc.) sans réécriture.

## 2. Vue d'ensemble

```
KUCIBOK SERVER
├── Dashboard
├── API
├── Prospector Engine
│   ├── Discovery Module
│   ├── Crawler Module
│   ├── Extraction Module
│   ├── Enrichment Module
│   ├── Intent Detection Module
│   ├── Scoring Module
│   ├── Deduplication Module
│   └── Storage Module
├── Outreach Engine            (nouveau)
│   ├── Persona Detector
│   ├── Message Generator
│   └── Sending Queue (dashboard, envoi manuel LinkedIn)
├── Artist Onboarding Module   (nouveau)
│   ├── Invitation Generator
│   ├── Contact Listener (webhook Instagram Business)
│   └── Auto-Enrollment (post-contact uniquement)
├── Local AI Engine
├── PostgreSQL
├── Job Queue / Workers
├── Scheduler
└── Monitoring / Logs
```

## 3. Stack technique

| Couche | Choix |
|---|---|
| Backend / API | Python + FastAPI |
| ORM | SQLAlchemy ou SQLModel |
| Migrations | Alembic |
| Base de données | PostgreSQL |
| Crawler | solution Python open source (requests/httpx + BeautifulSoup/lxml) |
| Browser automation | Playwright, uniquement si nécessaire (JS lourd) |
| IA locale | Ollama (ou équivalent), modèle interchangeable |
| Frontend / Dashboard | frontend minimal compatible FastAPI (ou React/Next.js si nécessaire) |
| Scheduler / Queue | Celery + Redis, ou APScheduler si suffisant pour la charge V1 |
| Conteneurisation | Docker + Docker Compose |
| Reverse proxy | Nginx ou Caddy (HTTPS) |

Règle : si une techno plus simple et open source fait le même travail, elle est préférée à une techno plus lourde.

## 4. Services Docker

- `app` — API FastAPI
- `worker` — jobs asynchrones (crawling, enrichissement, scoring)
- `database` — PostgreSQL
- `ai` — service Ollama (modèle local)
- `dashboard` — interface web
- `reverse-proxy` — Nginx/Caddy (HTTPS) si exposé publiquement

Chaque service est documenté dans `docker-compose.yml` avec ses variables d'environnement et volumes.

## 5. Abstraction AIProvider

```python
class AIProvider(ABC):
    def analyze(self, payload: dict) -> dict: ...
    def extract(self, text: str, schema: dict) -> dict: ...
    def classify(self, payload: dict) -> str: ...
    def summarize(self, text: str) -> str: ...

class LocalAIProvider(AIProvider):
    # implémentation via Ollama, modèle défini par MODEL_NAME (.env)
    ...

class ExternalAIProvider(AIProvider):
    # optionnel, désactivé par défaut, pour usage futur
    ...
```

Le nom du modèle n'est jamais codé en dur : il vient de la variable `MODEL_NAME` dans `.env`.

## 6. Modèle de données

### Table `prospects`

`id, type, name, country, city, website, email, linkedin, instagram, description, specialty, africa_interest, international_activity, digital_maturity, status, score, confidence, priority, recommended_angle, reason_to_contact, created_at, updated_at, last_verified_at`

`type` ∈ `{ARTIST, ART_ADVISOR, CURATOR, GALLERY, OTHER}`

### Table `sources`

`id, prospect_id, url, source_type, title, captured_text_hash, captured_at`

Règle : aucune information sans source associée.

### Table `signals`

`id, prospect_id, signal_type, description, source_url, signal_date, importance, confidence, created_at`

### Table `scores`

`id, prospect_id, score_type, score, breakdown, model_version, created_at`

`score_type` ∈ `{ARTIST_FIT, SAAS_FIT, CONFIDENCE, PRIORITY}`

### Table `searches`

`id, target_type, countries, keywords, volume, status, created_at, completed_at`

### Table `jobs`

`id, job_type, status, attempts, started_at, completed_at, error_message, result_count`

`status` ∈ `{PENDING, RUNNING, SUCCESS, FAILED, RETRYING}` — retry maximum : 3 tentatives.

### Table `job_errors`

Journalisation détaillée des erreurs par job (référence `job_id`, message, stack trace, timestamp).

### Table `ai_analyses`

Résultat brut structuré (JSON) de chaque appel `AIProvider.analyze()`, référencé au `prospect_id` et à la version du modèle utilisé.

### Table `messages` (nouveau)

`id, prospect_id, persona (ART_ADVISOR|CURATOR), variant_label, channel (LINKEDIN), content, status (DRAFT|SENT), generated_at, sent_at, model_version`

Génération automatique, aucun champ d'approbation — le contrôle humain se fait uniquement au moment de l'envoi manuel sur LinkedIn (hors système).

### Table `artist_contacts` (nouveau)

`id, prospect_id (type=ARTIST), instagram_handle, invitation_sent_at, first_contact_initiated_at, first_contact_channel, enrollment_status (INVITED|CONTACTED|ENROLLED), enrolled_at`

`first_contact_initiated_at` reste `NULL` tant que l'artiste n'a pas lui-même initié un contact (clic bio, réponse story, formulaire). C'est le verrou technique qui empêche toute création de compte avant confirmation de l'intéressé — cette colonne est la source de vérité, pas une simple donnée informative.

## 7. Discovery Engine

Génère des requêtes de recherche à partir de : cible, pays, secteur, mots-clés, signaux. Capable de produire automatiquement des variantes (ex. `"art advisor African contemporary art"`, `"gallery emerging African artists"`, `"Senegal contemporary artist"`).

## 8. Sécurité

- HTTPS obligatoire (reverse proxy)
- Authentification sur le dashboard, mots de passe hashés
- Toute configuration sensible en variables d'environnement (`.env`, jamais commité)
- PostgreSQL non exposé publiquement
- Firewall serveur
- Logs applicatifs
- Backups quotidiens automatisés

Fichier `.env.example` fourni, sans aucun secret réel.

## 9. Backup / Restore

```bash
scripts/backup.sh     # dump PostgreSQL quotidien, stocké localement
scripts/restore.sh     # restauration depuis un fichier de backup
```

Un redémarrage Docker ne doit jamais entraîner de perte de données (volumes persistants PostgreSQL).

## 10. Monitoring

Le dashboard/monitoring affiche : jobs réussis/échoués, prospects trouvés/enrichis, taux de doublons, temps moyen de traitement, erreurs récentes, CPU, RAM, stockage disque.

## 11. Scheduler — exemple de calendrier quotidien (configurable)

```
08:00  Discovery
09:00  Crawling
10:00  Enrichment
11:00  AI Analysis
12:00  Scoring
13:00  Database update
```

## 12. Coûts

Par défaut : LLM local, base de données locale, stockage local, crawler local, traitement local. Tout appel à un service externe payant est optionnel et désactivé par défaut.

## 13. Outreach Engine — contraintes d'intégration

- **Aucune connexion à un compte LinkedIn.** Le module ne fait qu'écrire dans la table `messages` et les afficher dans le dashboard. Pas de session LinkedIn, pas de cookie, pas de librairie d'automatisation LinkedIn dans les dépendances du projet — ce choix est volontaire et ne doit pas être "amélioré" plus tard sans revalidation explicite du risque de ban.
- Génération 100% automatique, déclenchée par le même scheduler que le scoring (section 11), pas d'étape de validation dans le workflow.

## 14. Artist Onboarding — intégration Instagram

- Utilise l'**API officielle Instagram Business Messaging** (Meta Graph API), pas de scraping/automatisation non-officielle du côté envoi.
- Un webhook Meta reçoit les événements de contact entrant (story reply, message, ou lien tracké en bio) et écrit `first_contact_initiated_at` dans `artist_contacts`.
- L'envoi automatisé (invitation de relance, complétion de profil, confirmation d'inscription) n'est déclenché par le worker que si `first_contact_initiated_at IS NOT NULL` — condition vérifiée systématiquement, pas seulement à la création.
- Le compte Instagram professionnel Kucibok doit être vérifié en tant que compte Business/Creator et connecté à une Page Meta pour accéder à cette API.
