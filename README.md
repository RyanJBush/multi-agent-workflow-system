# Multi-Agent Workflow Automation System

A production-oriented, full-stack **Multi-Agent Workflow Automation System** that accepts a research or planning task, routes it through a pipeline of specialized AI agents, and returns a structured, actionable result.

---

## Overview

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11+, FastAPI, Pydantic v2, SQLite (aiosqlite) |
| Agents | Modular agent classes with a shared base interface |
| Orchestration | Manual, transparent pipeline (Research → Summarizer → Planner) |
| Frontend | React 18, Vite, TypeScript, Tailwind CSS |
| Testing | pytest, ruff, httpx |
| CI | GitHub Actions |

---

## Quick Start

### 1. Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env        # adjust values as needed
uvicorn app.main:app --reload
```

API is available at **http://localhost:8000**  
Swagger UI: **http://localhost:8000/docs**

### 2. Frontend

```bash
cd frontend
npm install
cp ../.env.example .env.local  # set VITE_API_BASE_URL
npm run dev
```

Dashboard is available at **http://localhost:5173**

---


## Makefile Commands

```bash
make install
make lint
make format-check
make test
make type-check
make build
```

## Docker (Full Stack)

```bash
docker compose up --build
# backend: http://localhost:8000
# frontend: http://localhost:5173
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/workflows/run` | Submit a workflow task |
| GET | `/api/v1/workflows/history` | List past workflow runs |
| GET | `/api/v1/workflows/{id}` | Get a single run by ID |

---

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full design.

---

## Agent Pipeline

```
User Task
   │
   ▼
Research Agent     → structured findings (key facts, sources, gaps)
   │
   ▼
Summarizer Agent   → concise summary paragraph
   │
   ▼
Planner Agent      → prioritised action plan (numbered steps)
   │
   ▼
Aggregated Response (summary + plan + per-agent outputs + status)
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `development` | Runtime environment |
| `APP_PORT` | `8000` | Backend port |
| `LLM_PROVIDER` | `stub` | `stub` (deterministic mock) or `openai` |
| `OPENAI_API_KEY` | — | Required when `LLM_PROVIDER=openai` |
| `DATABASE_URL` | `sqlite+aiosqlite:///./workflows.db` | SQLite path |
| `VITE_API_BASE_URL` | `http://localhost:8000` | Frontend API base |

---

## Testing

```bash
# Backend
cd backend
pytest --tb=short -q

# Lint
ruff check app tests
ruff format --check app tests
```

---

## Project Structure

```
.
├── .env.example
├── .github/workflows/ci.yml
├── docs/ARCHITECTURE.md
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/          # FastAPI routers
│   │   ├── core/         # Config, logging
│   │   ├── schemas/      # Pydantic models
│   │   ├── agents/       # Agent implementations
│   │   ├── orchestration/# Pipeline logic
│   │   ├── services/     # LLM / external service abstraction
│   │   └── db/           # Database models & session
│   ├── tests/
│   └── requirements.txt
└── frontend/
    └── src/
        ├── components/
        ├── pages/
        ├── lib/
        ├── hooks/
        └── types/
```

---

## Resume Bullets

- Designed and implemented a **multi-agent workflow orchestration system** using FastAPI and Pydantic v2, featuring a transparent Research → Summarizer → Planner pipeline with structured JSON outputs.
- Built a **React/TypeScript/Tailwind** dashboard with real-time workflow submission, per-agent output cards, and persistent workflow history backed by SQLite.
- Abstracted LLM calls behind a provider interface supporting both a deterministic stub and OpenAI, enabling fully offline testing with 100 % test coverage.
- Configured **GitHub Actions CI** for automated linting (ruff), formatting checks, and pytest on every push and pull request.


## Demo Flow

1. Open the dashboard at `http://localhost:5173`.
2. Submit a research/planning task from the form.
3. Backend runs `Research -> Summarizer -> Planner` pipeline.
4. View per-agent structured outputs and final plan.
5. Open workflow history and inspect any prior run details.

## API Reference

- Health: `GET /health`
- Run workflow: `POST /api/v1/workflows/run`
- Workflow history: `GET /api/v1/workflows/history?limit=50`
- Workflow detail: `GET /api/v1/workflows/{id}`

See full examples in `docs/API_SPEC.md`.

## Deployment

### Docker compose (single host)

```bash
docker compose up --build -d
make smoke-test
```

### Production notes

- Set `LLM_PROVIDER=openai` and `OPENAI_API_KEY` for live model calls.
- Point `DATABASE_URL` to PostgreSQL in production.
- Restrict CORS origins from `*` to known frontend domains.
- Run behind a reverse proxy/load balancer (e.g., Nginx) with HTTPS.

## Limitations

- MVP uses sequential orchestration (no branching or retries).
- AuthN/AuthZ and multi-tenant isolation are not yet implemented.
- Observability is basic (structured logs + request IDs) and does not yet include tracing.

## Smoke Testing

```bash
make smoke-test
```

This checks backend health and validates one end-to-end workflow execution via API.
