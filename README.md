# Kroki Flask Generator

A Flask web application that provides a simple interface for generating diagrams using the [Kroki](https://kroki.io/) service. Supports multiple diagram types including Mermaid, PlantUML, and Graphviz with PNG and SVG output formats.

## ✨ Features

- **Web Interface**: Clean, responsive UI for diagram generation
- **Multiple Formats**: Support for Mermaid, PlantUML, and Graphviz diagrams
- **Flexible Output**: Generate PNG or SVG images
- **REST API**: HTTP API for programmatic diagram generation
- **Theme Support**: Configurable themes for Mermaid diagrams
- **Health Monitoring**: Built-in health checks with Kroki connectivity status
- **Docker Ready**: Complete containerization with Docker Compose
- **Production Ready**: Gunicorn WSGI server with proper error handling

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone and start the stack:**
```bash
git clone <repository-url>
cd create-graph
docker compose up --build
```

2. **Access the application:**
   - Web UI: http://localhost:8080
   - Health Check: http://localhost:8080/health
   - API: http://localhost:8080/api/generate

### Option 2: Local Development

1. **Prerequisites:**
   - Python 3.12+
   - Kroki service running (see [Kroki Installation](https://kroki.io/docs/setup/install/))

2. **Setup environment:**
```bash
# Clone repository
git clone <repository-url>
cd create-graph

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

3. **Configure environment:**
```bash
# Copy environment template
cp .env.template .env

# Edit .env with your settings
vim .env
```

4. **Run the application:**
```bash
# Development server
make run

# Or directly with Flask
python src/main.py
```

## ⚙️ Configuration

The application uses environment variables for configuration. Copy `.env.template` to `.env` and adjust as needed:

### Core Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `KROKI_URL` | `http://localhost:8000` | Kroki service endpoint |
| `REQUEST_TIMEOUT` | `10` | HTTP request timeout (seconds) |
| `MAX_BYTES` | `1000000` | Max diagram source size (bytes) |

### Flask Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_CONFIG` | `development` | Configuration mode (development/production/testing) |
| `FLASK_PORT` | `5000` | Flask server port |
| `FLASK_DEBUG` | `false` | Enable debug mode |
| `SECRET_KEY` | `dev-key-change-in-production` | Flask secret key |

### Theme Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `DIAGRAM_THEME` | `default` | Default diagram theme (default/light/dark/neutral/forest) |
| `DIAGRAM_BACKGROUND_COLOR` | `white` | Background color for diagrams |

## 📡 API Usage

### Generate Diagram (POST /api/generate)

**JSON Request:**
```bash
curl -X POST http://localhost:8080/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "diagram_type": "mermaid",
    "output_format": "png",
    "diagram_source": "graph TD\n    A[Start] --> B[Process]\n    B --> C[End]"
  }' \
  --output diagram.png
```

**Text Request:**
```bash
curl -X POST "http://localhost:8080/api/generate?diagram_type=plantuml&output_format=svg" \
  -H "Content-Type: text/plain" \
  -d "@startuml
      A -> B: Hello
      B -> C: World
      @enduml" \
  --output diagram.svg
```

**With Theme:**
```bash
curl -X POST http://localhost:8080/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "diagram_type": "mermaid",
    "output_format": "png",
    "diagram_source": "graph TD\n    A --> B",
    "diagram_theme": "dark"
  }' \
  --output diagram.png
```

### Health Check (GET /health)

```bash
curl http://localhost:8080/health
```

**Response:**
```json
{
  "service": "kroki-flask-generator",
  "version": "0.1.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "status": "healthy",
  "checks": {
    "service": {
      "status": "healthy",
      "message": "Flask service running"
    },
    "kroki": {
      "status": "healthy",
      "message": "Kroki service accessible at http://localhost:8000",
      "response_time_ms": 45
    }
  }
}
```

## 🎨 Supported Diagram Types

### Mermaid
```
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
```

### PlantUML
```
@startuml
actor User
participant System
User -> System: Request
System --> User: Response
@enduml
```

### Graphviz
```
digraph G {
    A -> B;
    B -> C;
    C -> A;
}
```

## 🐳 Docker Deployment

### Development
```bash
# Start full stack (app + kroki services)
docker compose up --build

# Start only the app (external Kroki)
docker compose up app
```

### Production
```bash
# Build production image
docker build -t kroki-flask-generator:latest .

# Run with external Kroki
docker run -d \
  --name kroki-app \
  -p 8080:8080 \
  -e KROKI_URL=http://your-kroki-service:8000 \
  -e FLASK_CONFIG=production \
  kroki-flask-generator:latest
```

## 🛠️ Development

### Available Commands
```bash
# Run development server
make run

# Run tests
make test

# Run linting
make lint

# Format code
make format

# Run integration tests
make test-integration

# Build Docker image
make docker-build
```

### Running Tests
```bash
# All tests
pytest

# Unit tests only
pytest -m "not integration"

# Integration tests only
pytest -m integration

# With coverage
pytest --cov=src --cov-report=html
```

### Code Quality
```bash
# Format with Black
black src tests

# Lint with Ruff
ruff check src tests

# Type checking
mypy src
```

## 🏗️ Architecture

```
├── src/                    # Application source code
│   ├── main.py            # Flask application factory
│   ├── config.py          # Configuration management
│   ├── routes.py          # Route definitions and handlers
│   └── kroki_client.py    # Kroki HTTP client
├── templates/             # Jinja2 templates
├── static/               # Static assets (CSS, JS)
├── tests/                # Test suite
├── scripts/              # Utility scripts
└── docker-compose.yml    # Container orchestration
```

### Key Components

- **Flask Application**: Web server and request handling
- **Kroki Client**: HTTP client for Kroki service communication
- **Config Management**: Environment-based configuration
- **Health Checks**: Service and dependency monitoring
- **Error Handling**: Comprehensive error responses
- **Theme Support**: Diagram styling and theming

## 🔧 Troubleshooting

### Common Issues

**Kroki Connection Failed**
- Verify Kroki service is running: `curl http://localhost:8000/health`
- Check `KROKI_URL` environment variable
- Ensure network connectivity in Docker setup

**Diagram Generation Timeout**
- Increase `REQUEST_TIMEOUT` value
- Check diagram complexity and size
- Verify Kroki service performance

**Invalid Diagram Syntax**
- Validate diagram syntax using online editors
- Check diagram type matches expected format
- Review error messages in logs

### Debug Mode

Enable debug logging:
```bash
export FLASK_DEBUG=true
export FLASK_CONFIG=development
python src/main.py
```

### Health Check Details

The `/health` endpoint provides detailed status information:
- **healthy**: All systems operational
- **degraded**: Some issues detected but service functional
- **unhealthy**: Critical issues affecting service

## 📄 License

[Add your license information here]

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📚 Additional Resources

- [Kroki Documentation](https://kroki.io/docs/)
- [Mermaid Syntax](https://mermaid-js.github.io/mermaid/)
- [PlantUML Guide](https://plantuml.com/)
- [Graphviz Documentation](https://graphviz.org/documentation/)