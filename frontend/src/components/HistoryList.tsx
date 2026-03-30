import type { WorkflowRunRecord } from '../types/workflow'

interface HistoryListProps {
  items: WorkflowRunRecord[]
  onSelect: (runId: string) => void
}

export default function HistoryList({ items, onSelect }: HistoryListProps) {
  if (items.length === 0) {
    return <p className="text-sm text-slate-500">No workflow history yet.</p>
  }

  return (
    <ul className="space-y-2">
      {items.map((item) => (
        <li key={item.run_id}>
          <button
            className="w-full rounded-lg border border-slate-200 p-3 text-left hover:bg-slate-50"
            onClick={() => onSelect(item.run_id)}
            type="button"
          >
            <p className="truncate text-sm font-medium text-slate-900">{item.summary || item.run_id}</p>
            <p className="text-xs text-slate-500">{new Date(item.created_at).toLocaleString()}</p>
          </button>
        </li>
      ))}
    </ul>
  )
}
