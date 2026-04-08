# Phase 6 — Testing Notes

## Added backend tests

- Health endpoint contract now verified for status payload and request-id response header.
- Workflow API roundtrip verified end-to-end (`run` -> `history` -> `detail`).
- Query validation failure covered for invalid history limit.
- Failure-path API behavior covered by forcing summarizer failure.
- Deterministic stub behavior covered by asserting stable outputs across repeated identical requests.

## Determinism strategy

- Tests use isolated SQLite temp DB per test fixture.
- LLM defaults to stub mode for reproducible outputs.
- Assertions avoid non-deterministic fields such as UUIDs and timestamps.
