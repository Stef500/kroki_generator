# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python Flask web application for generating diagrams using the Kroki service. The project is **production-ready** with comprehensive testing (85% coverage), CI/CD pipeline, and Docker deployment.

## Project Structure

```
create_graph/
├── src/                    # Main application code
│   ├── main.py            # Flask application factory
│   ├── routes.py          # API routes and web interface
│   ├── kroki_client.py    # HTTP client for Kroki service
│   └── config.py          # Environment-based configuration
├── tests/                  # Test suite (85% coverage)
│   ├── test_routes.py     # Flask routes tests
│   ├── test_kroki_client.py # HTTP client tests
│   ├── test_main.py       # Application factory tests
│   ├── test_config.py     # Configuration tests
│   └── test_integration.py # Docker integration tests
├── templates/              # Jinja2 templates
├── static/                 # CSS/JS assets
├── docs/                   # Documentation
│   └── DOCKERHUB_SETUP.md # DockerHub CI/CD configuration
├── scripts/                # Utility scripts
├── .github/workflows/      # GitHub Actions CI/CD
├── docker-compose.yml      # Development stack
├── Dockerfile             # Production container
└── pyproject.toml         # Python project configuration
```

## Development Commands

This project uses **uv** for fast dependency management:

### Environment Setup
```bash
# Install dependencies
uv sync --extra dev --extra test

# Run with uv
uv run python src/main.py
```

### Running the Application
```bash
# Development server
make run
# or
uv run python src/main.py

# Docker development stack
docker compose up --build
```

## Dependencies

**Production:**
- Flask 3.0+ (web framework)
- requests 2.31+ (HTTP client)
- python-dotenv 1.0+ (environment management)
- gunicorn 21.2+ (WSGI server)

**Development:**
- pytest 7.4+ with coverage (testing)
- black 23.0+ (code formatting)
- ruff 0.1+ (linting)
- pre-commit 3.4+ (git hooks)

## Architecture Notes

- **Web Framework**: Flask with Blueprint organization
- **HTTP Client**: Custom Kroki client with retry logic and error handling
- **Configuration**: Environment-based config with development/production/testing profiles
- **Testing**: Comprehensive test suite with mocks and integration tests
- **Deployment**: Docker containerization with multi-architecture support
- **CI/CD**: GitHub Actions with automated testing, linting, and DockerHub publishing

## Development Guidelines

- Follow Python 3.12+ syntax and features
- Use uv for dependency management (`uv sync`, `uv run`)
- Run tests before commits: `uv run pytest --cov=src`
- Use pre-commit hooks: `pre-commit install`
- Follow existing code style (black + ruff)
- Update tests when adding features (maintain ≥80% coverage)

## Production Deployment

### Docker (Recommended)
```bash
# Pull from DockerHub
docker pull YOUR-USERNAME/kroki-flask-generator:latest

# Run with environment config
docker run -d -p 8080:8080 \
  -e KROKI_URL=http://your-kroki:8000 \
  -e FLASK_CONFIG=production \
  YOUR-USERNAME/kroki-flask-generator:latest
```

### CI/CD Pipeline

- **Quality Gates**: Lint, format, test coverage ≥80%
- **Multi-Architecture**: AMD64 + ARM64 Docker builds
- **Automated Publishing**: DockerHub integration on main branch
- **Integration Testing**: Docker compose validation

## Quality Standards

- **Test Coverage**: 85% (exceeding 80% requirement)
- **Code Quality**: black formatting + ruff linting
- **Documentation**: Comprehensive docstrings and type hints
- **Container Security**: Non-root user, minimal attack surface

## Claude comportment
- quand tu finis une tâche, penses à mettre à jour le fichier TASKS.md
- prépare un message de commit clair et concis