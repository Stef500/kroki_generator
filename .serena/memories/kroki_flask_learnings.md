# Kroki Flask Generator - Technical Learnings

## Architecture Patterns Discovered

### Flask Application Factory
- Enables configuration flexibility for different environments
- Separates blueprint registration from app creation
- Facilitates testing with different configurations

### Kroki Service Integration
- **Preprocessing Strategy**: Modify diagram source before sending to Kroki
- **Theme Injection**: Use diagram-specific syntax for theming
- **Error Mapping**: Translate HTTP errors to user-friendly messages

## Key Technical Solutions

### Theme Implementation
**Problem**: Kroki generates diagrams with dark backgrounds by default
**Solution**: Preprocess diagram source to inject theme configuration

For Mermaid:
```
%%{init: {'theme': 'base'}}%%
[original source]
```

For PlantUML:
```
@startuml
!theme plain
skinparam backgroundColor white
[original source]
```

### Port Management
**Problem**: macOS AirPlay uses port 5000 by default
**Solution**: Environment-based port configuration
```python
port = int(os.getenv("FLASK_PORT", 5000))
```

### Docker Service Dependencies
**Problem**: Flask app starts before Kroki is ready
**Solution**: Health check dependencies in docker-compose
```yaml
depends_on:
  kroki:
    condition: service_healthy
```

## Development Workflow Optimizations

### Makefile Simplification
**Before**: 16 targets, unclear organization
**After**: 11 targets with clear categories:
- Development: install, dev, run
- Quality: test, lint, format  
- Production: docker, docker-stop
- Utils: clean, check

### Local Development Strategy
1. **Hybrid approach**: Docker for services (Kroki), local for Flask
2. **Benefits**: Fast iteration, easier debugging, service isolation
3. **Command**: `make dev` starts everything

## Error Handling Patterns

### Progressive Error Recovery
1. **Connection errors**: Inform user Kroki is unreachable
2. **Timeout errors**: Suggest service is slow
3. **HTTP 400**: Invalid diagram syntax
4. **HTTP 500**: Kroki service error

### Debugging Enhancement
Added comprehensive logging in routes:
```python
logger.error(f"Error type: {type(e)}")
logger.error(f"Traceback: {traceback.format_exc()}")
```

## Frontend Design Decisions

### Technology Choice
- **Bootstrap 5**: Rapid prototyping, responsive design
- **Vanilla JS**: Minimal complexity, no framework overhead
- **Form-based**: Simple interaction model

### UX Patterns
- **Progressive enhancement**: Works without JS
- **Real-time feedback**: Loading states, error messages
- **Download integration**: Direct file download from blob

## Docker Optimization

### Multi-stage Build
```dockerfile
FROM python:3.12-slim as builder
# Build dependencies

FROM python:3.12-slim as production  
# Runtime only
```

### Security Best Practices
- Non-root user execution
- Minimal base image
- Only runtime dependencies in final stage

## Configuration Management

### Environment-based Config
```python
class Config:
    KROKI_URL = os.getenv("KROKI_URL", "http://localhost:8000")
    DIAGRAM_BACKGROUND_COLOR = os.getenv("DIAGRAM_BACKGROUND_COLOR", "white")
```

### Development vs Production
- **Development**: Debug mode, local ports
- **Production**: Gunicorn, Docker networking
- **Environment switching**: Via FLASK_ENV

## Code Quality Patterns

### Error Class Hierarchy
```python
class KrokiError(Exception):
    """Base exception for Kroki-related errors."""
    pass
```

### Type Hints
```python
def generate_diagram(
    self, diagram_type: str, output_format: str, diagram_source: str
) -> Tuple[bytes, str]:
```

### Validation Strategy
- Input validation before processing
- Early return on invalid parameters
- Clear error messages for users

## Performance Considerations

### Request Handling
- **Direct requests**: For small diagrams
- **Temporary files**: For large payloads (>1MB)
- **Timeout management**: Configurable per environment

### Memory Management
```python
with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp_file:
    # Process large files without memory issues
```

## Lessons Learned

1. **Theme preprocessing** is more reliable than post-processing
2. **Service dependencies** require proper health checks in Docker
3. **Port conflicts** are common in development - make them configurable
4. **Error handling** should be user-friendly, not technical
5. **Makefile optimization** significantly improves developer experience