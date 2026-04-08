# API Specification (Phase 2)

Base URL (local): `http://localhost:8000`

Version prefix: `/api/v1`

## Health

### `GET /health`

#### Response `200`
```json
{
  "status": "ok",
  "service": "multi-agent-workflow-system",
  "version": "0.1.0"
}
```

---

## Run Workflow

### `POST /api/v1/workflows/run`

#### Request body
```json
{
  "task": "Create a go-to-market plan for a B2B analytics feature.",
  "metadata": {
    "priority": "high",
    "tags": ["product", "marketing"]
  }
}
```

#### Response `200`
```json
{
  "id": "9d0e34f2-72cc-4d7c-a775-34c574a9a8f9",
  "status": "success",
  "task": "Create a go-to-market plan for a B2B analytics feature.",
  "agent_results": [
    {
      "agent_name": "research",
      "status": "success",
      "output": {
        "key_findings": ["..."],
        "sources": ["..."]
      },
      "duration_ms": 180
    },
    {
      "agent_name": "summarizer",
      "status": "success",
      "output": {
        "summary": "..."
      },
      "duration_ms": 140
    },
    {
      "agent_name": "planner",
      "status": "success",
      "output": {
        "action_plan": ["..."]
      },
      "duration_ms": 160
    }
  ],
  "final_result": {
    "summary": "...",
    "action_plan": ["..."]
  },
  "created_at": "2026-04-07T00:00:00Z",
  "updated_at": "2026-04-07T00:00:01Z"
}
```

#### Error response `422`
```json
{
  "detail": [
    {
      "loc": ["body", "task"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

---

## Workflow History

### `GET /api/v1/workflows/history`

#### Query params (planned)
- `limit` (default `20`)
- `offset` (default `0`)
- `status` (`success|failed`, optional)

#### Response `200`
```json
{
  "items": [
    {
      "id": "9d0e34f2-72cc-4d7c-a775-34c574a9a8f9",
      "task": "Create a go-to-market plan for a B2B analytics feature.",
      "status": "success",
      "created_at": "2026-04-07T00:00:00Z",
      "updated_at": "2026-04-07T00:00:01Z"
    }
  ],
  "count": 1
}
```

---

## Workflow Detail

### `GET /api/v1/workflows/{id}`

#### Path params
- `id` (UUID)

#### Response `200`
- Same schema as `POST /api/v1/workflows/run` response.

#### Error response `404`
```json
{
  "detail": "Workflow not found"
}
```

---

## Data Contract Notes

- `agent_results[]` order is guaranteed to match execution order.
- `status` is currently `success|failed`; retries/degraded states are future extensions.
- `metadata` is optional and reserved for routing and prioritization strategies.
