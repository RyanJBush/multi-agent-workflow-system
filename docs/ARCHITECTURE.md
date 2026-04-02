# Architecture — Multi-Agent Workflow Automation System

## 1. System Overview

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend (React)                    │
│   WorkflowForm  ─►  AgentCards  ─►  FinalResultPanel    │
│         │                                  ▲            │
│         │  POST /api/v1/workflows/run       │            │
└─────────┼──────────────────────────────────┼────────────┘
          │                                  │
          ▼                                  │
┌─────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                     │
│                                                         │
│  Router (api/v1/workflows)                              │
│       │                                                 │
│       ▼                                                 │
│  Orchestrator.run(task)                                 │
│       │                                                 │
│       ├── ResearchAgent.run(task)  ──►  ResearchOutput  │
│       │                                                 │
│       ├── SummarizerAgent.run(research) ► SummaryOutput │
│       │                                                 │
│       └── PlannerAgent.run(summary)  ──►  PlanOutput   │
│                                                         │
│  WorkflowResponse (aggregated)                          │
│       │                                                 │
│       └── DB.save(run)  ──► SQLite (aiosqlite)         │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Agent Abstraction Strategy

Every agent inherits from `BaseAgent`:

```python
class BaseAgent(ABC):
    name: str
    description: str

    @abstractmethod
    async def run(self, input: AgentInput) -> AgentOutput: ...
```

Agent inputs and outputs are typed Pydantic models, making the contract
explicit and easy to validate or mock in tests.

The LLM call is isolated behind `LLMService`:

```python
class LLMService:
    async def complete(self, prompt: str) -> str: ...
```

In `stub` mode (default), `LLMService` returns deterministic templated
responses — no API key needed, fully testable offline.

---

## 3. Orchestration Pipeline

The `WorkflowOrchestrator` owns the sequential pipeline:

```
input (task str)
  └─► ResearchAgent  → ResearchFindings
        └─► SummarizerAgent  → Summary
              └─► PlannerAgent  → ActionPlan
                    └─► WorkflowResponse (aggregated)
```

Each stage output is passed as typed input to the next stage.
No framework magic — pure Python `async def` calls with `await`.

---

## 4. State & Persistence Strategy

- Workflow runs are persisted to SQLite via `aiosqlite`.
- The DB schema is created at startup if it does not exist.
- Each run stores: id (UUID), task, status, per-agent JSON, timestamps.
- History is queryable via `GET /api/v1/workflows/history`.

---

## 5. Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `app/api/` | FastAPI routers — input validation, response serialisation |
| `app/core/` | Config (pydantic-settings), app-level logging |
| `app/schemas/` | Pydantic request/response models shared across layers |
| `app/agents/` | BaseAgent + 3 concrete implementations |
| `app/orchestration/` | Pipeline coordinator |
| `app/services/` | LLMService abstraction (stub + openai provider) |
| `app/db/` | Async SQLite session, repository, run model |

---

## 6. Frontend Responsibilities

| Component | Responsibility |
|-----------|---------------|
| `WorkflowForm` | Controlled form; submits task to backend |
| `AgentOutputCard` | Renders a single agent's structured output |
| `FinalResultPanel` | Summary + action-plan in a readable layout |
| `HistoryList` | Fetches and displays past runs |
| `useWorkflow` hook | Encapsulates fetch lifecycle (idle/loading/success/error) |
| `lib/api.ts` | Typed API client wrapping `fetch` |

---

## 7. Config & Error Handling Strategy

- All config is loaded from `.env` via `pydantic-settings` — typed and validated at startup.
- FastAPI's built-in exception handler returns `{ "detail": "..." }` JSON for validation and HTTP errors.
- Agent errors are caught by the orchestrator in two ways: unhandled exceptions are caught by the `try/except` block, and non-success status values returned by an agent are checked explicitly — either path marks the run `failed` and stores the error message.
- The frontend propagates HTTP errors to a visible error banner.
- CORS is configured with `allow_origins=["*"]` for development. Credentials are not required — the frontend makes plain unauthenticated requests.
