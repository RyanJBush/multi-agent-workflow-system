import type {
  ApiError,
  WorkflowRequest,
  WorkflowResponse,
  WorkflowSummary,
} from "../types/workflow";

const BASE_URL = (import.meta.env.VITE_API_BASE_URL as string) || "http://localhost:8000";

function toMessage(error: ApiError, statusText: string): string {
  const rid = error.request_id ? ` (request: ${error.request_id})` : "";
  return `${error.detail || statusText}${rid}`;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const resp = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!resp.ok) {
    const body = (await resp.json().catch(() => ({ detail: resp.statusText }))) as ApiError;
    throw new Error(toMessage(body, resp.statusText));
  }

  return resp.json() as Promise<T>;
}

export const api = {
  runWorkflow: (payload: WorkflowRequest): Promise<WorkflowResponse> =>
    request<WorkflowResponse>("/api/v1/workflows/run", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  getHistory: (limit = 50): Promise<WorkflowSummary[]> =>
    request<WorkflowSummary[]>(`/api/v1/workflows/history?limit=${limit}`),

  getWorkflow: (id: string): Promise<WorkflowResponse> =>
    request<WorkflowResponse>(`/api/v1/workflows/${id}`),
};
