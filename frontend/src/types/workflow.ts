// Mirrors backend Pydantic schemas

export interface WorkflowRequest {
  task: string;
}

export interface ResearchFindings {
  key_facts: string[];
  gaps: string[];
  sources: string[];
  raw: string;
}

export interface SummaryOutput {
  summary: string;
  word_count: number;
}

export interface ActionStep {
  step: number;
  action: string;
  rationale: string;
}

export interface PlanOutput {
  steps: ActionStep[];
  estimated_duration: string;
}

export interface AgentResult {
  agent_name: string;
  status: "success" | "failed";
  output: ResearchFindings | SummaryOutput | PlanOutput | null;
  error: string | null;
  duration_ms: number;
}

export interface WorkflowResponse {
  id: string;
  task: string;
  status: "completed" | "failed";
  summary: string;
  action_plan: ActionStep[];
  agent_results: AgentResult[];
  created_at: string;
  completed_at: string | null;
  error: string | null;
}

export interface WorkflowSummary {
  id: string;
  task: string;
  status: "completed" | "failed";
  created_at: string;
  completed_at: string | null;
}

export interface ApiError {
  detail: string;
  request_id?: string;
}
