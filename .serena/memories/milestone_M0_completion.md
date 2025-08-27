# Milestone M0 - Scaffold - COMPLETED ✅

## Completed Tasks (4h)

### Structure projet (1.5h) ✅
- ✅ Repo + structure créés (`src/`, `tests/`, `pyproject.toml`)
- ✅ Dependencies ajoutées dans `pyproject.toml` (Flask, requests, pytest + dev tools)
- ✅ Configuration `.env.template` + loader dans `src/config.py`
  - KROKI_URL, REQUEST_TIMEOUT, MAX_BYTES configurés

### App Flask minimale (2h) ✅
- ✅ Bootstrap Flask (`wsgi.py`, `src/main.py` avec factory pattern)
- ✅ Routes de base (`src/routes.py`) avec blueprint pattern
- ✅ Page HTML template avec form complet
  - Template base avec Bootstrap 5
  - Form avec textarea, select diagrams/format, bouton génération
  - JavaScript frontend pour calls API (prêt pour M1)
  - Exemples Mermaid/PlantUML/Graphviz intégrés

### Outillage (0.5h) ✅
- ✅ Makefile avec targets `run`, `test`, `lint`, `format`, `docker-*`, `health`

## DoD Validation ✅
- ✅ App démarre localement (`GET /` returns 200)
- ✅ Health endpoint `/health` functional avec JSON response
- ✅ Lint OK (black + ruff configurés et passent)
- ✅ Structure prête pour M1 (routes API, client HTTP framework)

## Technical Architecture Implemented
```
src/
├── config.py          # Configuration avec .env loader
├── main.py             # Flask factory + WSGI entry
└── routes.py           # Blueprint avec routes principales

templates/
├── base.html           # Template de base Bootstrap 5
└── index.html          # UI complète avec form + JavaScript

Root/
├── wsgi.py             # Production WSGI entry point
├── Makefile            # Dev tooling automatisé
├── .env.template       # Configuration template
└── pyproject.toml      # Dependencies complètes
```

## Ready for M1 - Génération
- API route `/api/generate` définie dans frontend JS (prête pour backend)
- Validation forms frontend implémentée
- Client HTTP framework dans config prêt pour Kroki integration
- Error handling UI en place

## Development Commands Validated
```bash
uv pip install -e .           # Dependencies install OK
make lint                     # Code quality OK
make run                      # Dev server OK
make health                   # Health check OK
```