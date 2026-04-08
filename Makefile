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
