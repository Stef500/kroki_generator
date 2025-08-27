# Project Quality Standards and Testing Strategy

## Testing Architecture
- **Framework**: pytest with coverage reporting
- **Target**: ≥80% code coverage (achieved 85%)
- **Structure**: Unit tests + Integration tests with markers
- **Mocking**: requests-mock for HTTP client testing
- **Configuration**: pyproject.toml with pytest.ini_options

## Test Categories
1. **Unit Tests** (`tests/test_*.py`):
   - Routes: Flask endpoints and error handling
   - Client: HTTP client with timeout/retry logic
   - Config: Environment-based configuration
   - Main: Application factory pattern

2. **Integration Tests** (`@pytest.mark.integration`):
   - Docker compose stack testing
   - End-to-end diagram generation
   - Service health validation
   - Cross-service communication

## Quality Gates
- **Pre-commit**: black, ruff, pytest with coverage check
- **CI Pipeline**: Lint → Test → Coverage → Docker build
- **Coverage**: 85% achieved across all modules
- **Standards**: Type hints, docstrings, error handling

## Testing Patterns
- **Fixtures**: Flask test client, configuration objects
- **Mocking**: HTTP requests for external service isolation  
- **Error Testing**: Comprehensive error path coverage
- **Environment**: Testing config separate from production

## CI/CD Integration
- **GitHub Actions**: Multi-job pipeline with uv dependency management
- **Docker Testing**: Build verification and smoke tests
- **Parallel Execution**: Independent test and build jobs
- **Branch Protection**: Main branch requires passing tests

## Quality Tools
- **Formatter**: black (88 char line length)
- **Linter**: ruff with auto-fix
- **Coverage**: pytest-cov with term-missing report
- **Dependencies**: uv for fast, reliable package management

## Best Practices Established
- Test isolation with proper mocking
- Configuration testing for environment variables
- Integration test marking for optional execution
- Comprehensive error scenario coverage
- Docker integration for production-like testing