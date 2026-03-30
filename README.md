# Multi-Agent Workflow Automation System

This repository contains a production-oriented, portfolio-ready full-stack project built in incremental phases.

## Current Status

- ✅ Phase 1 (Planning) completed
- ✅ Phase 2 (Architecture) completed
- ✅ Phase 3 (Setup) completed
- ✅ Phase 4 (Backend) completed
- ✅ Phase 5 (Frontend) completed
- ✅ Phase 6 (Testing) completed
- ✅ Phase 7 (Deployment) completed

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+

### Backend

```bash
python -m venv .venv
source .venv/bin/activate
cd backend
pip install -e .[dev]
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173` and backend at `http://localhost:8000`.

## API Quick Check

```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/api/v1/workflows/run \
  -H "Content-Type: application/json" \
  -d '{
    "title": "US campus productivity app research",
    "objective": "Identify a practical go-to-market approach for first 90 days",
    "constraints": ["low budget", "small team"],
    "output_format": "both"
  }'
```

## Deployment

See `docs/PHASE_7_DEPLOYMENT.md` for:

- backend deployment steps
- frontend deployment steps
- recommended hosting split
- env var guidance
- demo checklist
- portfolio talking points
- resume bullets

## Phase Deliverables

- `docs/PHASE_1_PLAN.md`
- `docs/PHASE_2_ARCHITECTURE.md`
- `docs/PHASE_3_SETUP.md`
- `docs/PHASE_4_BACKEND.md`
- `docs/PHASE_5_FRONTEND.md`
- `docs/PHASE_6_TESTING.md`
- `docs/PHASE_7_DEPLOYMENT.md`
