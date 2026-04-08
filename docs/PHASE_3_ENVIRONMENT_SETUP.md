# Phase 3 — Environment Setup

## Delivered Tooling

- Root-level `Makefile` for reproducible install/lint/test/build/run workflows.
- Dockerized backend (`backend/Dockerfile`) and frontend (`frontend/Dockerfile`).
- Root `docker-compose.yml` for one-command full stack startup.
- Scoped environment templates:
  - `backend/.env.example`
  - `frontend/.env.example`
- CI enhancement to include frontend Prettier check.

## Reproducible Local Workflow

### Option A: Native local
```bash
make install
make lint
make format-check
make test
make type-check
make run-backend
make run-frontend
```

### Option B: Dockerized
```bash
docker compose up --build
```

## Determinism Notes

- Backend tests stay deterministic by defaulting to stub LLM mode.
- CI runs static checks and test commands in a fixed sequence.
- Docker images pin major runtimes (`python:3.11-slim`, `node:20-alpine`, `nginx:1.27-alpine`).

## Tradeoffs

- SQLite remains the default for simple local startup; production can swap `DATABASE_URL` to PostgreSQL.
- Docker Compose currently runs backend+frontend only to keep onboarding minimal.
- Makefile focuses on common commands and avoids environment-manager lock-in.
