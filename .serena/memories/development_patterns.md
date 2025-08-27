# Development Patterns & Best Practices

## Documentation Standards
- **Language**: French docstrings for all functions and classes
- **Format**: Google-style docstrings with Args, Returns, Raises sections
- **Type Hints**: Complete typing annotations using Optional, Tuple, etc.
- **Examples**: Practical usage examples in docstrings where helpful

## Code Organization
- **Factory Pattern**: Flask app creation with environment-based configuration
- **Blueprint Architecture**: Modular route organization
- **Configuration Classes**: Environment-specific config inheritance
- **Error Handling**: Custom exception classes with descriptive messages

## API Design
- **Flexible Input**: Support both JSON and text/plain content types
- **RESTful**: Clear HTTP status codes and response formats
- **Theme Support**: Dynamic theme injection for diagram preprocessing
- **Large Payloads**: Automatic handling via temporary files

## Testing Approach
- **Unit Tests**: Individual component testing with mocks
- **Integration Tests**: E2E testing with Docker containers
- **Pytest**: Modern testing framework with fixtures
- **Coverage**: Target ≥80% test coverage

## Quality Tools
- **Black**: Code formatting
- **Ruff**: Fast linting and code analysis
- **Pre-commit**: Automated quality checks
- **GitHub Actions**: CI/CD pipeline

## Docker Best Practices
- **Multi-stage builds**: Optimized production images
- **Non-root user**: Security-conscious container setup
- **Health checks**: Application and dependency monitoring
- **docker-compose**: Complete service orchestration

## File Naming Conventions
- **Source**: snake_case for Python modules
- **Documentation**: README.md, API_EXAMPLES.md
- **Configuration**: .env.template for environment examples
- **Scripts**: Descriptive names in scripts/ directory