# TASKS — Jalons & tâches

## M0 — Scaffold (4h détaillé) ✅ COMPLETED
### Structure projet (1.5h) ✅
- [x] Créer repo + structure (`src/`, `tests/`, `pyproject.toml`) (0.5h)
- [x] Setup dependencies avec Flask, requests, pytest dans `pyproject.toml` (0.5h) 
- [x] Configuration `.env.template` + loader dans `src/config.py` (0.5h)
  - `KROKI_URL=http://localhost:8000`
  - `REQUEST_TIMEOUT=10`
  - `MAX_BYTES=1000000`

### App Flask minimale (2h) ✅
- [x] Bootstrap Flask (`wsgi.py`, `src/main.py`) (0.5h) [dépend: structure]
- [x] Routes de base (`src/routes.py`) avec blueprint (0.5h) [dépend: bootstrap]
- [x] Page HTML template avec form Bootstrap 5 (1h) [dépend: routes]
  - Textarea pour diagramme
  - Select diagram_type (Mermaid, PlantUML, Graphviz)
  - Select output_format (PNG, SVG)
  - Bouton "Générer" + JavaScript frontend
  - Exemples intégrés + UI complète

### Outillage (0.5h) ✅
- [x] Makefile avec targets `run`, `test`, `lint`, `format`, `docker-*` (0.5h)

**DoD** ✅ : app démarre localement (`GET /` → 200, `/health` → JSON), lint OK (black+ruff).

## M1 — Génération (6h détaillé) ✅ COMPLETED
### Backend API (3h) ✅
- [x] Route `POST /api/generate` avec validation (1h) [dépend: M0.routes]
  - Support JSON `{diagram_type, output_format, diagram_source}`
  - Support `text/plain` + query params  
  - Schema validation + erreurs 400
- [x] Client HTTP vers Kroki (2h) [dépend: M0.config]
  - Headers `Content-Type: text/plain`, `Accept: image/*`
  - Gestion timeout + retry simple
  - Gestion payload volumineux → fichier temporaire si > MAX_BYTES

### Frontend (2h) ✅
- [x] UI affichage résultat image (1h) [dépend: backend]
  - Preview image inline (déjà implémenté en M0)
  - Gestion erreurs visuelles
- [x] Bouton téléchargement avec nom fichier (0.5h)
- [x] Messages d'erreur UX clairs (0.5h)
  - Type/format invalide
  - Timeout Kroki
  - Erreurs 5xx avec détails

### Validation (1h) ✅
- [x] Tests unitaires routes + client HTTP (1h)

**DoD** ✅ : MVP 3 types (Mermaid, PlantUML, Graphviz) → PNG/SVG OK ; erreurs UX lisibles.

## M2 — Dockerisation (3h détaillé) ✅ COMPLETED
### Conteneurisation (2h) ✅
- [x] `Dockerfile` production avec gunicorn (1h) [dépend: M1.backend]
  - Multi-stage build optimisé (builder + production)
  - User non-root (appuser)
  - COPY optimisé (layers) + .dockerignore
- [x] `docker-compose.yml` stack complète (1h)
  - Service app + kroki + mermaid
  - Networks et volumes appropriés
  - Variables d'environnement + healthchecks

### Robustesse (1h) ✅ 
- [x] Healthcheck avancé `/health` endpoint (0.5h)
  - Vérification connectivité Kroki + response time
  - Status JSON avec détails (healthy/degraded)
- [x] Tests intégration Docker (0.5h) [dépend: compose]
  - Smoke test + E2E génération via container
  - Script `./scripts/test-docker.sh` automatisé

**DoD** ✅ : `docker compose up --build` → UI `:8080` + génération E2E + healthcheck OK.

## M3 — Qualité & Tests (4h détaillé) 🔄 IN PROGRESS
### Documentation (2h) ✅ COMPLETED
- [x] README complet (1h) ✅
  - Setup local + Docker
  - Usage UI + API
  - Config variables
  - Troubleshooting & architecture
- [x] Docstring + type hints (1h) ✅
  - Docstrings détaillées en français pour tous les modules
  - Type hints complets avec typing.Optional, Tuple, etc.
  - Documentation des paramètres et valeurs de retour
- [x] Exemples curl (0.5h) ✅
  - API_EXAMPLES.md avec exemples complets
  - Tests de différents formats et cas d'erreur
  - Scripts batch et cas d'utilisation avancés

### Tests automatisés (2.5h)
- [ ] Tests unitaires complets ≥80% coverage (1.5h) [dépend: M1]
  - Routes + validation
  - Client HTTP + mocks  
  - Gestion erreurs (dont logging)
- [ ] Tests intégration marqués `integration` (1h) [dépend: M2]
  - E2E via docker-compose
  - Performance (payload large)
  - Robustesse (Kroki down)

### Qualité code (1.5h)
- [ ] Pre-commit hooks (black, ruff, pytest) (0.5h)
- [ ] CI pipeline GitHub Actions (1h)
  - Lint + unit tests
  - Integration tests (optionnel)
  - Coverage reporting
  - Push to Docker Hub (optionnel)

**DoD** : Pipeline CI vert + `pytest -m "integration"` passe + coverage ≥80%.

## M4 — Extras (optionnels, 3h)
### Extensions diagrammes (1.5h)
- [ ] Support types additionnels (0.5h par type)
  - BlockDiag, Ditaa, Excalidraw
  - SeqDiag, ActDiag, BPMN
  - **Priorité**: BlockDiag, Excalidraw (plus demandés)

### UX améliorée (1.5h)  
- [ ] Exemples rapides pré-chargés (0.5h)
  - Templates Mermaid/PlantUML cliquables
- [ ] Drag&drop fichier → auto-génération (0.5h)
- [ ] Historique session in-memory (0.5h)
  - Derniers 5 diagrammes générés

**DoD** : Features stables + docs README à jour + zéro régression MVP.