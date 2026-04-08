#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://localhost:8000}"

echo "[smoke] checking health endpoint..."
curl -fsS "$BASE_URL/health" > /tmp/health.json

TASK_PAYLOAD='{"task":"Create a 3-step launch plan for an AI knowledge base feature"}'

echo "[smoke] running workflow..."
curl -fsS -X POST "$BASE_URL/api/v1/workflows/run" \
  -H 'Content-Type: application/json' \
  -d "$TASK_PAYLOAD" > /tmp/workflow.json

echo "[smoke] verifying workflow response..."
python3 - <<'PY'
import json
from pathlib import Path

health = json.loads(Path('/tmp/health.json').read_text())
workflow = json.loads(Path('/tmp/workflow.json').read_text())

assert health.get('status') == 'ok', 'health status was not ok'
assert workflow.get('status') in {'completed', 'failed'}, 'workflow status missing'
assert 'agent_results' in workflow, 'agent_results missing'
assert len(workflow['agent_results']) >= 1, 'no agent results'
print('[smoke] success')
PY
