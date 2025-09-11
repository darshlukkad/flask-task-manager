# Flask Task Manager - Development Commands

.PHONY: help build run test test-coverage clean docker-build docker-test docker-run

help: ## Show this help message
	@echo "Flask Task Manager - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Local Development
install: ## Install dependencies
	pip install -r requirements.txt

run: ## Run the application locally
	python app.py

test: ## Run tests locally
	python -m pytest test_app.py -v

test-coverage: ## Run tests with coverage
	python -m pytest test_app.py --cov=app --cov-report=html --cov-report=term-missing

# Docker Commands
docker-build: ## Build Docker image
	docker build -t flask-task-manager .

docker-build-test: ## Build Docker image with tests
	docker build --target test -t flask-task-manager-test .

docker-run: ## Run Docker container
	docker run -p 5000:5000 flask-task-manager

docker-test: ## Run tests in Docker
	docker-compose run --rm test

docker-test-coverage: ## Run tests with coverage in Docker
	docker-compose run --rm test-coverage

docker-up: ## Start all services with Docker Compose
	docker-compose up --build

docker-down: ## Stop all services
	docker-compose down

# Production
docker-build-prod: ## Build production Docker image
	docker build --target production -t flask-task-manager:latest .

# Cleanup
clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

# CI/CD
ci-test: ## Run tests for CI/CD
	docker build --target test -t flask-task-manager-test .
	docker run --rm flask-task-manager-test
