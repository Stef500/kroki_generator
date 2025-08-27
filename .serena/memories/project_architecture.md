# Kroki Flask Generator - Architecture Overview

## Project Structure
```
create_graph/
├── src/                    # Application source code
│   ├── main.py            # Flask application factory
│   ├── config.py          # Configuration management
│   ├── routes.py          # Route definitions and handlers
│   └── kroki_client.py    # Kroki HTTP client
├── templates/             # Jinja2 templates
├── static/               # Static assets (CSS, JS)
├── tests/                # Test suite
├── scripts/              # Utility scripts
├── README.md             # Comprehensive documentation
├── API_EXAMPLES.md       # API usage examples
└── docker-compose.yml    # Container orchestration
```

## Key Components

### Flask Application (src/main.py)
- Factory pattern implementation
- Configuration-based app creation
- Blueprint registration
- Environment-aware setup

### Configuration (src/config.py)
- Environment-based configuration
- Development/Production/Testing configs
- Kroki service settings
- Theme and styling options

### Route Handlers (src/routes.py)
- Main UI endpoint (/)
- Health check with Kroki connectivity (/health)
- Diagram generation API (/api/generate)
- JSON and text/plain support
- Comprehensive error handling

### Kroki Client (src/kroki_client.py)
- HTTP client for Kroki service
- Theme preprocessing for Mermaid/PlantUML
- Large payload handling with temp files
- Robust error handling and retry logic
- Support for multiple diagram types and formats

## Supported Features
- **Diagram Types**: Mermaid, PlantUML, Graphviz
- **Output Formats**: PNG, SVG
- **Themes**: Default, light, dark, neutral, forest
- **Request Formats**: JSON, text/plain with query params
- **Health Monitoring**: Advanced health checks with service connectivity
- **Docker**: Full containerization with docker-compose

## Quality Standards
- 100% documented with French docstrings
- Complete type hints throughout codebase  
- Comprehensive API examples
- Error handling for all failure scenarios
- Production-ready Docker configuration