import type { WorkflowHistoryResponse, WorkflowRequest, WorkflowResult } from '../types/workflow'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let details = ''

    try {
      const payload = (await response.json()) as { message?: string; detail?: string }
      details = payload.message ?? payload.detail ?? ''
    } catch {
      details = ''
    }

    const suffix = details ? `: ${details}` : ''
    throw new Error(`API request failed (${response.status})${suffix}`)
  }

  return (await response.json()) as T
}

export async function runWorkflow(payload: WorkflowRequest): Promise<WorkflowResult> {
  const response = await fetch(`${API_BASE}/api/v1/workflows/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  return handleResponse<WorkflowResult>(response)
}

export async function fetchWorkflowHistory(limit = 20): Promise<WorkflowHistoryResponse> {
  const response = await fetch(`${API_BASE}/api/v1/workflows/history?limit=${limit}`)
  return handleResponse<WorkflowHistoryResponse>(response)
}

export async function fetchWorkflowRun(runId: string): Promise<{ response_payload: WorkflowResult }> {
  const response = await fetch(`${API_BASE}/api/v1/workflows/${runId}`)
  return handleResponse<{ response_payload: WorkflowResult }>(response)
}
