# Phase 2 — Architecture

## 1) Architecture Summary

The system uses a **modular monorepo** with a React frontend and FastAPI backend.

- Frontend sends a workflow request to backend (`POST /api/v1/workflows/run`).
- Backend orchestrator executes three agents in sequence:
  1. Research Agent
  2. Summarizer Agent
  3. Planner Agent
- Aggregated output is persisted to SQLite and returned as a structured response.
- Frontend renders per-agent outputs, final summary, and action plan.

Design priorities:
- explicit module boundaries
- deterministic data contracts (Pydantic + TypeScript types)
- local-first developer experience
- easy extension to more agents/workflows later

---

## 2) Backend Module Responsibilities

### `app/main.py`
- App bootstrap, router registration, middleware, startup hooks.

### `app/api/`
- Thin HTTP layer only.
- Parse request, call service/orchestrator, map exceptions to HTTP responses.
- Routes:
  - `GET /health`
  - `POST /api/v1/workflows/run`
  - `GET /api/v1/workflows/history`
  - `GET /api/v1/workflows/{run_id}`

### `app/schemas/`
- Pydantic request/response models.
- Enforces typed agent output and final workflow output schema.

### `app/agents/`
- `base.py`: shared `Agent` protocol/interface.
- `research_agent.py`: generate findings structure.
- `summarizer_agent.py`: produce concise summary from findings.
- `planner_agent.py`: produce prioritized action items.

### `app/orchestration/`
- Workflow orchestrator coordinates agent sequence and dependency passing.
- Handles partial-failure behavior and status reporting.

### `app/services/`
- Service layer around orchestration and persistence.
- Keeps API layer thin and testable.

### `app/db/`
- SQLite connection/bootstrap.
- Repository functions for create/list/get workflow runs.

### `app/core/`
- Environment config (`BaseSettings`), app constants, custom exceptions, logging helpers.

---

## 3) Frontend Component/Page Responsibilities

### `pages/DashboardPage.tsx`
- Main view container.
- Composes form, run output, and history panel.

### `components/WorkflowForm.tsx`
- Collects user request/context.
- Triggers run submission.

### `components/AgentOutputPanel.tsx`
- Displays each agent’s structured output in readable cards.

### `components/FinalResultPanel.tsx`
- Shows summary + prioritized action plan + overall status.

### `components/HistoryList.tsx`
- Lists prior runs with timestamp/status; allows selecting run detail.

### `lib/api.ts`
- Backend HTTP client wrappers.

### `hooks/useWorkflow.ts`
- UI state management for submit/load/error/result transitions.

### `types/workflow.ts`
- Shared frontend types mirroring backend response contracts.

---

## 4) Workflow Data Flow

1. User submits `{title, objective, constraints?, audience?, output_format?}`.
2. API validates request against Pydantic schema.
3. `WorkflowService` creates `run_id` and calls orchestrator.
4. Orchestrator executes:
   - Research Agent with original request
   - Summarizer Agent with research output
   - Planner Agent with summary + research output
5. Orchestrator aggregates outputs into canonical `WorkflowResult`.
6. Service persists run record in SQLite.
7. API returns structured response to frontend.
8. Frontend renders:
   - per-agent cards
   - final summary/action plan
   - status + run metadata

---

## 5) Agent Abstraction Strategy

Use a simple, explicit interface:

- `AgentInput` and `AgentOutput` typed models.
- `Agent` protocol with:
  - `name: str`
  - `run(input: AgentInput) -> AgentOutput`

Why this approach:
- high interview clarity
- low complexity for MVP
- easy to mock for tests
- future-ready for plugging in real LLM provider clients

No heavy agent framework for MVP unless extension later requires graph branching.

---

## 6) State and Persistence Strategy

### Backend state
- Stateless request handling in API/service/orchestrator.
- Persistent run history in SQLite for demo and audit trail.

### SQLite schema (simple)
- `workflow_runs`
  - `run_id` (text primary key)
  - `created_at` (timestamp)
  - `status` (text)
  - `request_payload` (json text)
  - `response_payload` (json text)
  - `error_message` (nullable text)

### Frontend state
- Local component/hook state only (no Redux needed).
- States: `idle | submitting | success | error`.

---

## 7) Configuration Strategy

Environment-based config via `.env` and `pydantic-settings`:

- `APP_NAME`
- `APP_ENV` (`local`, `dev`, `prod`)
- `API_PREFIX` (default `/api/v1`)
- `SQLITE_PATH` (default `./backend/workflows.db`)
- `LLM_MODE` (`mock` default)
- `LLM_API_KEY` (optional for future provider integration)
- `FRONTEND_ORIGIN` (CORS)

This keeps local setup simple and production migration straightforward.

---

## 8) Error Handling Strategy

- Validation errors: automatic 422 from FastAPI/Pydantic.
- Domain failures (agent/orchestration): custom exceptions mapped to 4xx/5xx envelopes.
- API response envelope includes:
  - `status`
  - `message`
  - `run_id` (if available)
  - `details` (optional)
- Persist failed runs with status `failed` and error message for post-mortem visibility.

---

## 9) Why This Architecture Is Scalable + Recruiter-Friendly

1. **Clear layering** (API → service → orchestration → agents → db) signals production engineering discipline.
2. **Typed contracts** on backend/frontend reduce integration defects.
3. **Modular agent interface** enables adding agents/workflows without rewriting core flow.
4. **Persistence built-in** gives demo credibility and supports basic analytics later.
5. **Local-first simplicity** keeps scope realistic for one-week execution while still looking enterprise-minded.
