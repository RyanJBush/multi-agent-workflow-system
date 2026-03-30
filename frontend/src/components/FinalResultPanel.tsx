import type { WorkflowResult } from '../types/workflow'

interface FinalResultPanelProps {
  result: WorkflowResult | null
}

export default function FinalResultPanel({ result }: FinalResultPanelProps) {
  if (!result) {
    return <p className="text-sm text-slate-500">Run a workflow to view summary and action plan.</p>
  }

  return (
    <section className="space-y-4">
      <div>
        <p className="text-xs uppercase tracking-wide text-slate-500">Workflow Status</p>
        <p className="text-sm font-medium text-slate-900">{result.status}</p>
      </div>

      <div>
        <p className="text-xs uppercase tracking-wide text-slate-500">Summary</p>
        <p className="mt-1 text-sm text-slate-800">{result.summary || 'No summary generated.'}</p>
      </div>

      <div>
        <p className="text-xs uppercase tracking-wide text-slate-500">Action Plan</p>
        {result.action_plan.length === 0 ? (
          <p className="mt-1 text-sm text-slate-500">No action items available.</p>
        ) : (
          <ul className="mt-2 space-y-2">
            {result.action_plan.map((item, index) => (
              <li key={`${item.task}-${index}`} className="rounded-lg border border-slate-200 p-3">
                <p className="text-sm font-semibold text-slate-900">{item.task}</p>
                <p className="text-xs text-slate-600">Priority: {item.priority}</p>
                <p className="mt-1 text-sm text-slate-700">{item.rationale}</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  )
}
