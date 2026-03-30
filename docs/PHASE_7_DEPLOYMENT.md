# Phase 7 — Deployment

## Recommended hosting split (student-friendly)

- **Backend (FastAPI):** Render Web Service (or Railway)
- **Frontend (Vite React):** Vercel (or Netlify)
- **Database:** SQLite for local demos. For public deployment, either:
  - keep SQLite only for single-instance demos, or
  - switch to managed Postgres in next iteration.

## Exact deployment steps

### 1) Prepare backend for hosting

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Backend start command for Render/Railway:

```bash
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 2) Configure backend environment variables

- `APP_NAME`
- `APP_ENV=prod`
- `API_PREFIX=/api/v1`
- `SQLITE_PATH=./workflows.db`
- `FRONTEND_ORIGIN=<your-frontend-url>`
- `LLM_MODE=mock`
- `LLM_API_KEY` (optional)

### 3) Deploy frontend

```bash
cd frontend
npm install
npm run build
npm run preview
```

Frontend env var:

- `VITE_API_BASE_URL=<your-backend-url>`

### 4) Verify deployed system

- Open frontend URL.
- Submit workflow request.
- Validate final result + per-agent outputs.
- Open history and verify persisted run appears.

## Production README improvements (included)

- Added deployment commands and environment setup guidance.
- Added demo checklist.
- Added portfolio talking points and resume bullet examples.

## Demo checklist

- [ ] Backend health endpoint returns `{"status":"ok"}`
- [ ] Workflow run endpoint returns 3 agent outputs
- [ ] Action plan and summary render in UI
- [ ] History list updates after each run
- [ ] Project README has local + deployment instructions

## Portfolio talking points

1. Designed and built a modular multi-agent orchestration platform with typed contracts.
2. Implemented clean backend layering (API/service/orchestration/agents/db).
3. Built a frontend dashboard that visualizes per-agent traceability and outcomes.
4. Added persistence and workflow run history for reproducible demos and debugging.
5. Shipped a production-oriented MVP with testing and deployment documentation.

## Resume bullet suggestions

- Built a full-stack Multi-Agent Workflow Automation System (FastAPI + React/TypeScript) that orchestrates specialized AI agents to convert raw briefs into structured summaries and action plans.
- Implemented typed API contracts (Pydantic + TS), modular orchestration architecture, and SQLite-backed workflow history for traceable runs.
- Developed a SaaS-style dashboard for workflow submission, per-agent output inspection, and historical run retrieval.
- Added backend test coverage for API routes, schema validation, and orchestration behavior; documented deployment for public demos.
