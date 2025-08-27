# TASKS — Jalons & tâches

## M0 — Scaffold (4h détaillé)
### Structure projet (1.5h)
- [ ] Créer repo + structure (`src/`, `tests/`, `pyproject.toml`) (0.5h)
- [ ] Setup `requirements.txt` avec Flask, requests, pytest (0.5h) 
- [ ] Configuration `.env` template + loader (0.5h)
  - `KROKI_URL=http://localhost:8000`
  - `REQUEST_TIMEOUT=10`
  - `MAX_BYTES=1000000`

### App Flask minimale (2h)
- [ ] Bootstrap Flask (`wsgi.py`, `src/app.py`) (0.5h) [dépend: structure]
- [ ] Routes de base (`src/routes.py`) (0.5h) [dépend: bootstrap]
- [ ] Page HTML template avec form (1h) [dépend: routes]
  - Textarea pour diagramme
  - Select diagram_type (Mermaid, PlantUML, Graphviz)
  - Select output_format (PNG, SVG)
  - Bouton "Générer"

### Outillage (0.5h)
- [ ] Makefile avec targets `run`, `test`, `lint` (0.5h)

**DoD** : app démarre localement (`GET /` OK), lint OK.

## M1 — Génération (6h détaillé)
### Backend API (3h)
- [ ] Route `POST /api/generate` avec validation (1h) [dépend: M0.routes]
  - Support JSON `{diagram_type, output_format, diagram_source}`
  - Support `text/plain` + query params
  - Schema validation + erreurs 400
- [ ] Client HTTP vers Kroki (2h) [dépend: M0.config]
  - Headers `Content-Type: text/plain`, `Accept: image/*`
  - Gestion timeout + retry simple
  - Gestion payload volumineux → fichier temporaire si > MAX_BYTES

### Frontend (2h)
- [ ] UI affichage résultat image (1h) [dépend: backend]
  - Preview image inline
  - Gestion erreurs visuelles
- [ ] Bouton téléchargement avec nom fichier (0.5h)
- [ ] Messages d'erreur UX clairs (0.5h)
  - Type/format invalide
  - Timeout Kroki
  - Erreurs 5xx avec détails

### Validation (1h)
- [ ] Tests unitaires routes + client HTTP (1h)

**DoD** : MVP 3 types (Mermaid, PlantUML, Graphviz) → PNG/SVG OK ; erreurs UX lisibles.

## M2 — Dockerisation (3h détaillé)
### Conteneurisation (2h)
- [ ] `Dockerfile` production avec gunicorn (1h) [dépend: M1.backend]
  - Multi-stage build optimisé
  - User non-root
  - COPY optimisé (layers)
- [ ] `docker-compose.yml` stack complète (1h)
  - Service app + kroki + mermaid
  - Networks et volumes appropriés
  - Variables d'environnement

### Robustesse (1h) 
- [ ] Healthcheck avancé `/health` endpoint (0.5h)
  - Vérification connectivité Kroki
  - Status JSON avec détails
- [ ] Tests intégration Docker (0.5h) [dépend: compose]
  - Smoke test génération via container

**DoD** : `docker compose up --build` → UI `:8080` + génération E2E + healthcheck OK.

## M3 — Qualité & Tests (4h détaillé)
### Tests automatisés (2.5h)
- [ ] Tests unitaires complets ≥80% coverage (1.5h) [dépend: M1]
  - Routes + validation
  - Client HTTP + mocks  
  - Gestion erreurs
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