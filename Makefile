# PDF AI Application - Docker Management

.PHONY: help build up down logs clean test

.DEFAULT_GOAL := help

help: ## Show help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build Docker images
	docker-compose build

up: ## Start services
	docker-compose up -d
	@echo "App: http://localhost:8000"

down: ## Stop services  
	docker-compose down

logs: ## Show logs
	docker-compose logs -f

restart: ## Restart services
	docker-compose restart

clean: ## Clean containers and volumes
	docker-compose down -v
	docker system prune -f

test: ## Run tests
	docker-compose exec app python -m pytest tests/ -v

shell: ## Open app shell
	docker-compose exec app bash

db-shell: ## Open database shell
	docker-compose exec mariadb mysql -u pdf_user -p pdf_ai_db

status: ## Show status
	docker-compose ps