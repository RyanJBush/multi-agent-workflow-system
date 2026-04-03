export type Priority = 'high' | 'medium' | 'low'

export interface WorkflowRequest {
  title: string
  objective: string
  constraints: string[]
  audience?: string
  output_format: 'action_plan' | 'brief' | 'both'
}

export interface ActionItem {
  task: string
  priority: Priority
  rationale: string
}

export interface AgentResult {
  agent_name: string
  status: 'completed' | 'failed'
  output: Record<string, unknown>
}

export interface WorkflowResult {
  run_id: string
  status: 'completed' | 'failed'
  created_at: string
  summary: string
  action_plan: ActionItem[]
  agent_results: AgentResult[]
  error_message: string | null
}

export interface WorkflowRunRecord {
  run_id: string
  status: string
  created_at: string
  summary: string
}

export interface WorkflowHistoryResponse {
  items: WorkflowRunRecord[]
}
