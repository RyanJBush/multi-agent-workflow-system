SHELL := /bin/bash
.PHONY: help dev-backend dev-frontend test lint build up down logs

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

# ── Local development ───────────────────────────────────────────────────────

dev-backend: ## Run the backend dev server with hot-reload
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Run the frontend dev server
	cd frontend && npm run dev

# ── Quality gates ──────────────────────────────────────────────────────────

test: ## Run the backend test suite
	cd backend && pytest --tb=short -q

lint: ## Lint and format-check backend (ruff) + frontend (eslint, tsc)
	cd backend && ruff check app tests && ruff format --check app tests
	cd frontend && npm run lint && npm run type-check

# ── Docker ─────────────────────────────────────────────────────────────────

build: ## Build all Docker images
	docker compose build

up: ## Start all services in detached mode
	docker compose up -d

down: ## Stop and remove containers
	docker compose down

logs: ## Tail logs from all running services
	docker compose logs -f
