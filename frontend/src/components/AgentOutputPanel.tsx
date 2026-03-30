import type { AgentResult } from '../types/workflow'

interface AgentOutputPanelProps {
  agentResults: AgentResult[]
}

export default function AgentOutputPanel({ agentResults }: AgentOutputPanelProps) {
  if (agentResults.length === 0) {
    return <p className="text-sm text-slate-500">No agent outputs yet.</p>
  }

  return (
    <div className="grid gap-3">
      {agentResults.map((agent) => (
        <article key={agent.agent_name} className="rounded-lg border border-slate-200 bg-slate-50 p-4">
          <div className="mb-2 flex items-center justify-between">
            <h3 className="text-sm font-semibold text-slate-900">{agent.agent_name}</h3>
            <span className="rounded bg-emerald-100 px-2 py-1 text-xs text-emerald-700">
              {agent.status}
            </span>
          </div>
          <pre className="overflow-x-auto text-xs text-slate-700">
            {JSON.stringify(agent.output, null, 2)}
          </pre>
        </article>
      ))}
    </div>
  )
}
