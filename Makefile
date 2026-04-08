SHELL := /bin/bash
.DEFAULT_GOAL := help

PYTHON ?= python3
PIP ?= pip
BACKEND_DIR := backend
FRONTEND_DIR := frontend

help:
	@echo "Available commands:"
	@echo "  make install            - install backend + frontend dependencies"
	@echo "  make install-backend    - install backend dependencies"
	@echo "  make install-frontend   - install frontend dependencies"
	@echo "  make lint               - run backend ruff + frontend eslint"
	@echo "  make format-check       - run backend/frontend format checks"
	@echo "  make test               - run backend pytest"
	@echo "  make type-check         - run frontend TypeScript checks"
	@echo "  make build              - build frontend assets"
	@echo "  make run-backend        - run FastAPI locally"
	@echo "  make run-frontend       - run Vite locally"
	@echo "  make docker-up          - start full stack via Docker Compose"
	@echo "  make docker-down        - stop Docker Compose stack"
	@echo "  make smoke-test         - run API smoke tests against a running backend"

install: install-backend install-frontend

install-backend:
	cd $(BACKEND_DIR) && $(PIP) install -r requirements.txt

install-frontend:
	cd $(FRONTEND_DIR) && npm ci

lint:
	cd $(BACKEND_DIR) && ruff check app tests
	cd $(FRONTEND_DIR) && npm run lint

format-check:
	cd $(BACKEND_DIR) && ruff format --check app tests
	cd $(FRONTEND_DIR) && npm run format:check

test:
	cd $(BACKEND_DIR) && pytest --tb=short -q

type-check:
	cd $(FRONTEND_DIR) && npm run type-check

build:
	cd $(FRONTEND_DIR) && npm run build

run-backend:
	cd $(BACKEND_DIR) && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run-frontend:
	cd $(FRONTEND_DIR) && npm run dev -- --host 0.0.0.0 --port 5173

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down


smoke-test:
	./scripts/smoke_test.sh
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
