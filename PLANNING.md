# PLANNING — Vision, Architecture, Stack & Outils

## Vision courte
- App **Flask** minimaliste + client HTTP vers **Kroki** local.
- **Dockerisable**, portable, testée (unit + intégration).

## Architecture détaillée

### Vue d'ensemble
```
[Client Browser] → [Flask Routes] → [Kroki Client] → [Kroki Server]
       ↓              ↓                ↓              ↓
   [UI Feedback] ← [Error Handler] ← [HTTP Client] ← [Response]
       ↑
   [Download]
```

### Flux de données
1. **UI Input** : Utilisateur colle diagramme + sélectionne type/format
2. **Validation** : Schema check côté Flask (diagram_type, format, taille)
3. **Routing** : `POST /api/generate` → service interne
4. **Kroki Call** : `POST {KROKI_URL}/{diagram_type}/{output_format}`
   - Headers : `Content-Type: text/plain`, `Accept: image/png|image/svg+xml`
   - Fallback fichier temporaire si payload > MAX_BYTES
5. **Response** : Image binaire → UI display + download button

### Gestion d'état
- **Session** : Historique in-memory (derniers diagrammes générés)
- **Cache** : Pas de cache persistant (stateless)
- **Logs** : Erreurs + métriques sans contenu sensible

### Stratégie erreurs
- **Client** : Messages UX clairs (timeout, format invalide, Kroki indispo)
- **Server** : Codes HTTP appropriés (400, 502, 500) + logs structurés
- **Monitoring** : Healthcheck `/health` avec status Kroki

## Stack technique
- **Python** 3.11+ with uv package manager ; **Flask**, **gunicorn** (prod), **requests**.
- **Tests** : pytest, pytest-cov, requests-mock ; intégration avec Kroki via compose.
- **Qualité** : black, ruff, pre-commit.
- **Conteneurs** : Docker, docker-compose.
- **Config** : `.env` → `KROKI_URL` (def. `http://kroki:8000`), `REQUEST_TIMEOUT=10`, `MAX_BYTES=1000000`.

## Outils requis
- Docker / Docker Compose, Python 3.11+, curl, make (option).

## Fichiers clés proposés
### `Dockerfile`
```dockerfile
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY wsgi.py .
ENV FLASK_ENV=production
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]
```

### `docker-compose.yml`
```yaml
services:
  app:
    build: .
    environment:
      - KROKI_URL=http://kroki:8000
      - REQUEST_TIMEOUT=10
      - MAX_BYTES=1000000
    ports:
      - "8080:8080"
    depends_on: [kroki]
  kroki:
    image: yuzutech/kroki
    depends_on: [mermaid]
    environment:
      - KROKI_MERMAID_HOST=mermaid
      - KROKI_MERMAID_PORT=8002
    ports: ["8000:8000"]
  mermaid:
    image: yuzutech/kroki-mermaid
    expose: ["8002"]
```

## Endpoints (app)
- `GET /` : page HTML (textarea, selects, bouton).
- `POST /api/generate` : JSON `{diagram_type, output_format, diagram_source}` **ou** `text/plain` (+ query/headers).

## Tests
- **Unit** : validation params, construction requêtes, gestion erreurs & timeouts.
- **Intégration** : compose (kroki + mermaid) + appels réels `/api/generate`.
- Marqueur : `-m "integration"`.

## Déploiement
### Environnements
- **Dev** : `docker compose up --build` (kroki + mermaid local)
- **Prod** : Dockerfile gunicorn + env vars externes  
- **CI** : GitHub Actions (lint → unit → integration optionnelle)

### Pipeline qualité
1. **Lint** : black + ruff (pre-commit hooks)
2. **Unit** : pytest avec mocks Kroki
3. **Integration** : tests E2E avec stack Docker
4. **Coverage** : ≥80% requis pour merge

## Sécurité & Performance

### Sécurité
- **Input validation** : Schema strict pour diagram_source (pas d'injection)
- **Limits** : MAX_BYTES payload, REQUEST_TIMEOUT pour DoS protection  
- **Logs** : Pas de stockage contenu utilisateur, logs d'erreur sobres
- **Headers** : CORS approprié pour API, pas d'exposition interne

### Performance
- **Timeout strategy** : 10s par défaut, configurable via env
- **Payload handling** : Stream vers fichier temporaire si > 1MB
- **Monitoring** : Métriques génération (succès/échec, latence)

## Documentation
- README concis (setup, exemples `curl`, capture d’écran), table des codes d’erreur.
