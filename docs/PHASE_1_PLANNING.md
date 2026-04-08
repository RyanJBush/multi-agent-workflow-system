# Phase 1 — Planning

## 1) Users

### Primary users
- **Operations managers / project leads** who need structured task breakdowns quickly.
- **Analysts / researchers** who need repeatable synthesis from broad prompts.
- **Small engineering or product teams** who want a lightweight internal workflow assistant.

### Secondary users
- **Platform engineers** extending orchestration rules and providers.
- **Hiring managers / recruiters** reviewing engineering quality (portfolio and ATS relevance).

---

## 2) Problem Statement

Teams often process ambiguous tasks manually: gather context, summarize key insights, and build an actionable plan. This process is inconsistent, hard to audit, and difficult to scale.

We need a production-oriented system that:
- accepts free-form user tasks,
- routes work through explicit specialized agents,
- returns structured, explainable outputs,
- persists workflow history for traceability,
- and presents a modern dashboard suitable for daily use.

---

## 3) MVP Scope (Phase 1 definition)

### In scope
1. **Submit task**
   - User inputs a task from the dashboard.
   - Backend validates and initiates workflow.

2. **Run deterministic pipeline**
   - Orchestrated sequence: **Research → Summarizer → Planner**.
   - Each agent returns typed output for consistency.

3. **Store workflow history**
   - Save request payload, per-agent outputs, final summary, and status.
   - PostgreSQL-ready schema with SQLite local development defaults.

4. **Retrieve past run details**
   - History endpoint for list view.
   - Detail endpoint for full run inspection by ID.

5. **Show structured outputs in UI**
   - Agent output cards.
   - Final summary + plan section.
   - Basic loading/error/empty states.

### Explicitly non-goals for MVP
- Autonomous branching/delegation trees.
- Long-running distributed queues.
- Multi-tenant auth/permissions.
- Fine-grained role-based access.

---

## 4) Stretch Goals

1. **Tool integrations**
   - Web/file connectors and retrieval abstractions.
2. **Retry/failure states**
   - Per-agent retries, degraded-mode completion, richer failure reasons.
3. **Observability traces**
   - OpenTelemetry spans and request-to-workflow correlation.
4. **Additional agents**
   - Critic/validator, risk assessor, estimator, executor, or compliance checker.

---

## 5) Product and Engineering Success Criteria

### Product success
- User can submit a task and receive structured outputs in one interaction.
- History is queryable and usable for retrospective review.
- Interface is understandable without onboarding.

### Engineering success
- Strong schema validation at API boundaries.
- Deterministic stub mode for repeatable testing.
- Clear agent interfaces and explainable orchestration path.
- Local dev can be bootstrapped quickly and reproduced in CI.

---

## 6) Risks and Mitigations

1. **Prompt/output drift across providers**
   - Mitigation: strict Pydantic contracts + normalization layer.

2. **Brittle orchestration coupling**
   - Mitigation: explicit `BaseAgent` interface + orchestration service boundaries.

3. **Unclear failure diagnostics**
   - Mitigation: structured logging, request IDs, standardized error envelope.

4. **Portfolio polish vs. velocity tradeoff**
   - Mitigation: define MVP early and defer complexity to stretch backlog.

---

## 7) MVP Acceptance Criteria (Definition of Done for core app)

- [ ] `POST /api/v1/workflows/run` accepts validated task input and returns structured pipeline result.
- [ ] Workflow executes in strict order: Research → Summarizer → Planner.
- [ ] Workflow and outputs are persisted and retrievable by history/detail endpoints.
- [ ] Frontend dashboard can submit tasks, render outputs, and browse history.
- [ ] Deterministic tests cover success and key failure paths.

---

## 8) ATS-Relevant Project Positioning

This project demonstrates:
- multi-agent orchestration design,
- typed API and data contracts,
- full-stack delivery with React + FastAPI,
- CI/testing discipline,
- deployment readiness with Docker and environment strategy,
- and real-world engineering structure beyond toy scripts.
