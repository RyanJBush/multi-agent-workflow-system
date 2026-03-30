# Phase 6 — Testing

## Commands

```bash
cd backend && pytest -q
cd backend && ruff check .
cd backend && ruff format --check .
cd frontend && npm run lint
```

## Implemented tests

- API tests
  - `test_health.py`
  - `test_workflow_api.py`
- Schema validation tests
  - `test_schema_validation.py`
- Orchestration structure tests
  - `test_orchestrator.py`

## Coverage focus for MVP

- endpoint health/status
- workflow submission and history retrieval
- schema input validation behavior
- orchestrator response structure and agent sequencing

## Not yet covered (future expansion)

- frontend component/unit tests
- backend failure-path tests for simulated agent exceptions
- repository-level edge cases (pagination, malformed payload recovery)
