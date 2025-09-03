.PHONY: help install dev run test lint format docker docker-stop clean check

help: ## Show this help message
	@echo 'Usage: make <target>'
	@echo ''
	@echo 'Development:'
	@echo '  install    Install dependencies (dev + test)'
	@echo '  dev        Start everything for development (Flask + Kroki)'
	@echo '  run        Run Flask only (requires Kroki separately)'
	@echo ''
	@echo 'Quality:'
	@echo '  test       Run all tests with coverage'
	@echo '  lint       Check code quality'
	@echo '  format     Auto-format code'
	@echo ''
	@echo 'Production:'
	@echo '  docker       Run production with Docker Compose'
	@echo '  docker-build Build Docker image locally'
	@echo '  docker-test  Test Docker image locally'
	@echo '  docker-stop  Stop Docker services'
	@echo ''
	@echo 'Utils:'
	@echo '  clean      Clean temporary files'
	@echo '  check      Health check'

# === DÉVELOPPEMENT ===

install: ## Install dependencies (dev + test)
	uv pip install -e .[test,dev]

dev: ## Start everything for development (Flask + Kroki)
	@echo "Starting Kroki services..."
	docker compose up -d kroki mermaid
	@echo "Waiting for Kroki to be ready..."
	@sleep 3
	@echo "Starting Flask application..."
	PYTHONPATH=. FLASK_PORT=5001 uv run python src/main.py

run: ## Run Flask only (requires Kroki separately)
	PYTHONPATH=. FLASK_PORT=5001 python src/main.py

# === QUALITÉ ===

test: ## Run all tests with coverage
	uv run pytest tests/ -v --cov=src --cov-report=term-missing

lint: ## Check code quality
	uv run black --check src tests
	uv run ruff check src tests

format: ## Auto-format code
	uv run black src tests
	uv run ruff check --fix src tests

# === PRODUCTION ===

docker: ## Run production with Docker Compose
	docker compose up --build

docker-build: ## Build Docker image locally
	docker build -t kroki-flask-generator:latest .

docker-test: ## Test Docker image locally  
	./scripts/test-docker-build.sh

docker-stop: ## Stop Docker services
	docker compose down

# === UTILS ===

clean: ## Clean temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

check: ## Health check
	curl -f http://localhost:5001/health || echo "Service not running"