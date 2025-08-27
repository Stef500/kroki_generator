.PHONY: help install run test lint clean dev-install

help: ## Show this help message
	@echo 'Usage: make <target>'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install production dependencies
	uv pip install -e .

dev-install: ## Install development dependencies
	uv pip install -e .[test,dev]

run: ## Run the Flask development server
	python src/main.py

test: ## Run tests with coverage
	pytest tests/ -v --cov=src --cov-report=term-missing

lint: ## Run code quality checks
	black --check src tests
	ruff check src tests

format: ## Format code with black and ruff
	black src tests
	ruff check --fix src tests

clean: ## Clean up temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

docker-build: ## Build Docker image
	docker build -t kroki-flask-generator .

docker-run: ## Run with Docker Compose
	docker compose up --build

docker-down: ## Stop Docker Compose
	docker compose down

health: ## Check application health
	curl -f http://localhost:5000/health || echo "Service not running"

docker-test: ## Run Docker integration tests
	./scripts/test-docker.sh

integration-test: ## Run integration tests only (requires running services)
	pytest tests/test_integration.py -v -m integration

smoke-test: ## Quick smoke test of running services
	pytest tests/test_integration.py -v -k "not integration"