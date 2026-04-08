# Phase 2 — Architecture

## 1) Monorepo Design

```text
multi-agent-workflow-system/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI route modules and API versioning
│   │   ├── core/             # settings, logging, request context, errors
│   │   ├── db/               # engine/session, models, repositories, migrations-ready
│   │   ├── schemas/          # shared Pydantic contracts for requests/responses
│   │   ├── agents/           # BaseAgent + concrete agents
│   │   ├── orchestration/    # workflow orchestrator + execution policies
│   │   └── services/         # LLM provider abstractions and adapters
│   ├── tests/
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── pages/
│   │   └── types/
│   └── package.json
├── docs/
│   ├── PHASE_1_PLANNING.md
│   ├── PHASE_2_ARCHITECTURE.md
│   ├── API_SPEC.md
│   └── ARCHITECTURE.md
└── .github/workflows/
```

### Rationale
- Keep backend and frontend independently testable/releasable while sharing a single repository lifecycle.
- Keep boundaries explicit so orchestration logic never leaks into transport/controller code.

---

## 2) Backend Module Contracts

## `app/api`
- Input/output translation layer only.
- No agent logic; delegates to orchestration/services.
- Versioned under `/api/v1` for compatibility evolution.

## `app/core`
- Configuration and environment loading.
- Logging setup (JSON-ready structure in production).
- Request context hooks (request IDs / timing) and centralized exception mapping.

## `app/db`
- Persistence model and repository access.
- PostgreSQL-ready model design (UUID ids, JSON columns, timestamps) while allowing SQLite local execution.

## `app/agents`
- Isolated agent implementations.
- Enforced by `BaseAgent` interface to preserve substitutability and testability.

## `app/orchestration`
- Pipeline coordinator (Research → Summarizer → Planner).
- Applies execution order, state transitions, and error propagation strategy.

## `app/services`
- LLM abstraction boundary.
- Supports deterministic stub mode and OpenAI-compatible provider mode.

## `app/schemas`
- Shared typed contracts crossing API, orchestration, and persistence boundaries.

---

## 3) Common Agent Interface

```python
from abc import ABC, abstractmethod
from app.schemas.workflow import AgentExecutionContext, AgentResult

class BaseAgent(ABC):
    name: str
    version: str = "1.0"

    @abstractmethod
    async def run(self, context: AgentExecutionContext) -> AgentResult:
        """Execute agent logic and return typed, serializable output."""
```

### Interface requirements
- **Deterministic shape:** every agent returns the same top-level result envelope.
- **Explainability:** each result includes structured data + concise narrative.
- **Observability-ready:** each run emits timing metadata and optional warnings.

---

## 4) Orchestrator Service Design

### Responsibility
A single service (`WorkflowOrchestrator`) that:
1. validates initial workflow input,
2. executes agents in fixed order,
3. transforms outputs between stages,
4. persists intermediate/final state,
5. returns aggregated typed response.

### Execution policy
- Default policy: **sequential deterministic pipeline**.
- Failure policy: fail-fast for MVP, recording failing stage and reason.
- Extension point: retry strategy and conditional branching as post-MVP additions.

### Orchestrator output
- `workflow_id`
- `status` (`success | failed`)
- `agent_results[]` in execution order
- `final_summary`
- timestamps (`started_at`, `completed_at`)

---

## 5) Data Contracts

## Workflow request
```json
{
  "task": "string",
  "metadata": {
    "priority": "low|medium|high",
    "tags": ["string"]
  }
}
```

## Per-agent result
```json
{
  "agent_name": "research|summarizer|planner",
  "status": "success|failed",
  "input": {},
  "output": {},
  "started_at": "ISO-8601",
  "completed_at": "ISO-8601",
  "duration_ms": 0,
  "error": null
}
```

## Final summary
```json
{
  "summary": "string",
  "action_plan": ["step 1", "step 2"],
  "confidence": 0.0
}
```

## Workflow history item
```json
{
  "id": "uuid",
  "task": "string",
  "status": "success|failed",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601"
}
```

---

## 6) API Endpoints (v1)

- `GET /health`
  - returns service health and version metadata.

- `POST /api/v1/workflows/run`
  - accepts workflow request payload.
  - returns full workflow response (agent outputs + final summary).

- `GET /api/v1/workflows/history`
  - returns paginated/sorted history list (MVP can default to recent-first limit).

- `GET /api/v1/workflows/{id}`
  - returns one workflow run including all agent outputs.

---

## 7) Architecture Decisions (ADR-style summary)

1. **Layered backend with strict module boundaries**
   - improves maintainability and test isolation.

2. **Typed contracts everywhere (Pydantic)**
   - reduces integration bugs and improves API reliability.

3. **Stub-first LLM provider abstraction**
   - ensures deterministic CI without external API dependencies.

4. **PostgreSQL-ready persistence with SQLite local default**
   - balances production readiness with easy onboarding.

5. **Sequential explainable orchestration as MVP default**
   - maximizes transparency and debuggability over novelty.
