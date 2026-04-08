import type { WorkflowSummary } from "../types/workflow";

interface Props {
  history: WorkflowSummary[];
  loading: boolean;
  error: string | null;
  selectedId: string | null;
  onSelect: (id: string) => void;
  onRefresh: () => void;
}

export function HistoryList({ history, loading, error, selectedId, onSelect, onRefresh }: Props) {
  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-base font-semibold text-gray-800">Recent Workflows</h2>
        <button
          onClick={onRefresh}
          className="text-xs text-indigo-600 hover:text-indigo-800 font-medium"
        >
          Refresh
        </button>
      </div>

      {loading && <p className="text-sm text-gray-400">Loading history…</p>}
      {error && <p className="text-sm text-red-500">{error}</p>}

      {!loading && !error && history.length === 0 && (
        <p className="text-sm text-gray-400 italic">No workflows run yet.</p>
      )}

      <ul className="space-y-2 max-h-[24rem] overflow-y-auto pr-1">
        {history.map((item) => {
          const isActive = selectedId === item.id;
          return (
            <li
              key={item.id}
              onClick={() => onSelect(item.id)}
              className={`cursor-pointer rounded-lg border px-4 py-3 transition-all ${
                isActive
                  ? "border-indigo-400 bg-indigo-50 shadow-sm"
                  : "border-gray-200 bg-white hover:border-indigo-300 hover:shadow-sm"
              }`}
            >
              <div className="flex items-start justify-between gap-2">
                <p className="text-sm font-medium text-gray-800 line-clamp-2 flex-1">{item.task}</p>
                <span
                  className={`flex-shrink-0 text-xs font-medium px-2 py-0.5 rounded-full ${
                    item.status === "completed"
                      ? "bg-green-100 text-green-700"
                      : "bg-red-100 text-red-700"
                  }`}
                >
                  {item.status}
                </span>
              </div>
              <p className="text-xs text-gray-400 mt-1">
                {new Date(item.created_at).toLocaleString()}
              </p>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
