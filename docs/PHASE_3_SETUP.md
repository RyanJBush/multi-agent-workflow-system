# Phase 3 — Setup

## Completed Setup Scope

- Initialized backend structure for FastAPI app and tests.
- Added Python packaging/dependency config via `backend/pyproject.toml`.
- Added root `.env.example`, `.gitignore`, `.editorconfig`, and `Makefile`.
- Initialized React + Vite + TypeScript + Tailwind frontend baseline.
- Added ESLint and Prettier script configuration.
- Added minimal starter code:
  - FastAPI health endpoint
  - frontend starter dashboard shell

## Run Commands

### Backend
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
cd backend && pip install -e .[dev] && cd ..
uvicorn backend.app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Verification

- Backend health endpoint: `curl http://localhost:8000/health` should return `{"status":"ok"}`.
- Frontend should load `http://localhost:5173` and display “Phase 3 setup complete”.
