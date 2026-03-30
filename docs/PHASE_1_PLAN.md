# Phase 1 — Planning

## 1) Concise Project Overview

Build a **Multi-Agent Workflow Automation System** that acts like an internal AI operations assistant. A user submits a business research/brief request, and the system orchestrates specialized agents (Research, Summarizer, Planner) to return a structured outcome suitable for execution.

The MVP focuses on one excellent workflow, strong API and UI clarity, and production-style engineering practices that are realistic for a 3–7 day build.

---

## 2) Target User / Use Case

### Primary user persona
- **Operations intern / junior PM / startup founder / analyst** who needs to quickly turn a raw request into an actionable plan.

### Core use case
- User submits a prompt such as: *“Research entry strategy for a student productivity app in US colleges.”*
- System returns:
  - key findings
  - concise summary
  - prioritized action plan
  - per-agent output trace

---

## 3) Core Features (MVP In Scope)

1. **Workflow submission** via backend API and frontend form.
2. **Orchestration layer** that coordinates three agents in sequence.
3. **Typed agent outputs** and typed final workflow response.
4. **Health check endpoint** for operational readiness.
5. **Workflow run history (SQLite)** for demo/replay value.
6. **Dashboard UI** to run workflows and inspect results/history.
7. **Basic quality tooling**: linting, formatting, and backend tests.

---

## 4) Non-Goals (Out of Scope for MVP)

1. Multi-user authentication/authorization.
2. Real-time collaboration or websocket streaming.
3. Complex distributed queues/event buses.
4. Fine-tuning/custom model training.
5. Advanced tool integrations (Slack/Jira/Notion) in v1.
6. Deep observability stack (Prometheus/Grafana/OpenTelemetry).

These are great future extensions but unnecessary for a one-week portfolio MVP.

---

## 5) MVP Success Criteria

Project is considered successful if:

1. User can submit a workflow request from UI and receive a structured result.
2. At least 3 agents execute through a transparent orchestrator.
3. API responses are validated, typed, and consistent.
4. Workflow run is stored and retrievable from history endpoint/UI.
5. App runs locally with clear setup docs in <15 minutes.
6. Includes tests + linting, and has clean repo organization recruiters can scan quickly.

---

## 6) Chosen Workflow and Agent Roles

### Workflow name
**Research-to-Action Workflow**

### Agent roles
1. **Research Agent**
   - Input: user request
   - Output: structured findings (bullet insights, assumptions, risks)

2. **Summarizer Agent**
   - Input: research findings
   - Output: concise executive summary

3. **Planner Agent**
   - Input: summary + findings
   - Output: prioritized action plan (tasks with rationale and priority)

### Final response shape
- workflow metadata (run_id, timestamps, status)
- normalized summary
- action plan list
- per-agent outputs
- optional warnings/errors

---

## 7) Proposed Final Folder Structure

```text
multi-agent-workflow-system/
  README.md
  .gitignore
  .editorconfig
  .env.example
  Makefile
  backend/
    pyproject.toml
    app/
      main.py
      api/
        routes_health.py
        routes_workflows.py
      core/
        config.py
        logging.py
        exceptions.py
      schemas/
        workflow.py
      agents/
        base.py
        research_agent.py
        summarizer_agent.py
        planner_agent.py
      orchestration/
        workflow_orchestrator.py
      services/
        workflow_service.py
      db/
        sqlite.py
        repository.py
    tests/
      test_health.py
      test_workflow_api.py
      test_orchestrator.py
  frontend/
    package.json
    vite.config.ts
    tsconfig.json
    index.html
    src/
      main.tsx
      App.tsx
      pages/
        DashboardPage.tsx
      components/
        WorkflowForm.tsx
        AgentOutputPanel.tsx
        FinalResultPanel.tsx
        HistoryList.tsx
      lib/
        api.ts
      hooks/
        useWorkflow.ts
      types/
        workflow.ts
      styles/
        index.css
```

---

## 8) Implementation Plan (Phases 2–7)

### Phase 2 — Architecture
- Define backend module contracts and frontend component responsibilities.
- Specify orchestration data flow and error model.
- Finalize persistence shape and environment strategy.

### Phase 3 — Setup
- Initialize backend (FastAPI, ruff, pytest) and frontend (Vite React TS Tailwind).
- Add .env.example, .gitignore, Makefile, starter README sections.
- Confirm local run commands.

### Phase 4 — Backend
- Build health + workflow endpoints.
- Implement agent interfaces and concrete agents.
- Build orchestration + response aggregation.
- Add SQLite run history endpoints.

### Phase 5 — Frontend
- Build dashboard and form.
- Render agent outputs, final summary, action plan.
- Add workflow history list + run detail interaction.
- Add loading/error/empty/success states.

### Phase 6 — Testing
- Add API and orchestration tests.
- Add schema validation tests.
- Wire lint/format/test scripts.

### Phase 7 — Deployment
- Add deployment instructions (backend + frontend split).
- Add env guidance + demo checklist.
- Add portfolio talking points and resume bullets.

---

## 9) Why This Project Is High-Signal for Recruiters

1. Demonstrates **agent orchestration design**, not just a chatbot wrapper.
2. Shows **full-stack product thinking**: usable UI + reliable backend contracts.
3. Uses **professional engineering practices**: modular architecture, typed schemas, tests, linting.
4. Presents a **clear business workflow** with measurable value and easy demo story.
5. Is intentionally scoped to finish fast while leaving room for meaningful extensions.
