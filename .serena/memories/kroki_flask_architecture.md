# Kroki Flask Generator - Architecture Understanding

## Project Vision
Flask-based web application for generating diagram images (PNG/SVG) from text descriptions using local Kroki service.

## Core Architecture
```
[Client Browser] → [Flask Routes] → [Kroki Client] → [Kroki Server]
       ↓              ↓                ↓              ↓
   [UI Feedback] ← [Error Handler] ← [HTTP Client] ← [Response]
       ↑
   [Download]
```

## Technology Stack
- **Backend**: Python 3.11+, Flask, gunicorn (production)
- **Client**: requests library for HTTP calls to Kroki
- **Testing**: pytest, pytest-cov, requests-mock
- **Quality**: black, ruff, pre-commit hooks
- **Deployment**: Docker, docker-compose
- **Services**: Kroki + Mermaid companion containers

## Key Features Planned
### MVP (M0-M3)
- 3 diagram types: Mermaid, PlantUML, Graphviz
- 2 output formats: PNG, SVG
- Web UI + REST API
- Docker deployment
- 80%+ test coverage

### Post-MVP (M4)
- Extended diagram types: BlockDiag, Ditaa, Excalidraw
- PDF output support
- UI enhancements (drag-drop, examples, history)

## Critical Design Decisions
- **Stateless**: No persistent storage, session-only history
- **File handling**: Temporary files for large payloads (>1MB)
- **Error strategy**: Clear UX messages, proper HTTP codes
- **Security**: Input validation, payload limits, timeout protection
- **Monitoring**: Health endpoint, structured logs, metrics

## Development Approach
- 17h total effort across 4 milestones
- Progressive enhancement (scaffold → generation → docker → quality)
- Dependency-aware task planning
- Integration testing with full Docker stack