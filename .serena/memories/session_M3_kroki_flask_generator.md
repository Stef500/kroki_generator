# Session M3 - Kroki Flask Generator Development

## Project Overview
Created a complete Flask-based diagram generation service using Kroki as backend. The project provides a web interface for generating Mermaid, PlantUML, and Graphviz diagrams with theme support and customizable background colors.

## Key Achievements

### 1. Flask Application Setup
- Created Flask application factory pattern in `src/main.py`
- Implemented configuration management with `src/config.py`
- Set up production-ready WSGI configuration

### 2. Kroki Integration
- Built `src/kroki_client.py` with comprehensive error handling
- Implemented theme preprocessing for Mermaid (base, dark, neutral, forest)
- Added PlantUML styling with white background support
- Created robust HTTP client with timeout and connection error handling

### 3. Web Interface
- Developed responsive Bootstrap-based UI in `templates/`
- Added diagram type selector (Mermaid, PlantUML, Graphviz)
- Implemented theme selection and background color customization
- Created real-time diagram generation with error handling

### 4. Development Environment
- Configured Docker Compose with Kroki, Mermaid, and Flask services
- Optimized Makefile from 16 to 11 targets (31% reduction)
- Set up development workflow with `make dev` command
- Implemented health checks and service dependencies

### 5. Production Readiness
- Multi-stage Dockerfile with security best practices
- Complete Docker Compose setup for one-command deployment
- Environment configuration with .env support
- Comprehensive error handling and logging

## Technical Decisions

### Architecture
- **Pattern**: Flask application factory
- **Client**: Custom Kroki HTTP client with preprocessing
- **Frontend**: Bootstrap 5 with vanilla JavaScript
- **Deployment**: Docker Compose orchestration

### Theme Implementation
- **Mermaid**: Preprocessed theme injection via `%%{init: {'theme': 'base'}}%%`
- **PlantUML**: Skinparam injection for white background
- **UI**: Dynamic background color application

### Port Configuration
- **Development**: Flask on 5001 (avoiding macOS AirPlay conflict)
- **Production**: Flask on 8080, Kroki on 8000
- **Internal**: Docker network communication

## File Structure
```
src/
├── main.py          # Flask application factory
├── config.py        # Configuration management
├── routes.py        # API and web routes
└── kroki_client.py  # Kroki service client

templates/
├── base.html        # Base template with Bootstrap
└── index.html       # Main interface

Dockerfile           # Multi-stage production build
docker-compose.yml   # Complete service orchestration
Makefile            # Optimized development commands
```

## Key Code Patterns

### Theme Preprocessing (Mermaid)
```python
def _preprocess_mermaid(self, source: str) -> str:
    theme_config = f"%%{{init: {{'theme': '{mermaid_theme}'}}}}%%\n"
    return theme_config + source
```

### Error Handling
```python
except requests.exceptions.ConnectionError:
    raise KrokiError("Connection error - Cannot reach Kroki service")
```

### Docker Health Checks
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
```

## Deployment Commands

### Development
```bash
make dev        # Start Kroki + Flask
make run        # Flask only
make install    # Dependencies
```

### Production
```bash
docker compose up    # Complete deployment
```

## Resolved Issues
1. **Port conflict**: Changed from 5000 to 5001 for development
2. **Theme support**: Implemented preprocessing for diagram themes
3. **Error handling**: Added comprehensive connection and timeout handling
4. **Makefile complexity**: Reduced from 16 to 11 organized targets
5. **Docker networking**: Proper service dependencies and health checks

## Next Steps for M4
- Integration testing setup
- Performance optimization
- Additional diagram types support
- Advanced theme customization
- API documentation