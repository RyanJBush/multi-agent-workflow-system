import type { WorkflowResponse } from "../types/workflow";

interface Props {
  result: WorkflowResponse;
}

export function FinalResultPanel({ result }: Props) {
  return (
    <div className="rounded-xl border border-indigo-200 bg-indigo-50 p-6 space-y-6">
      <div className="flex items-start justify-between gap-4">
        <h2 className="text-lg font-bold text-indigo-900">Workflow Result</h2>
        <span
          className={`text-xs font-semibold px-3 py-1 rounded-full ${
            result.status === "completed"
              ? "bg-green-100 text-green-700"
              : "bg-red-100 text-red-700"
          }`}
        >
          {result.status}
        </span>
      </div>

      {result.error && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg p-3">
          {result.error}
        </p>
      )}

      {result.summary && (
        <div>
          <h3 className="text-sm font-semibold text-indigo-700 uppercase tracking-wide mb-2">
            Summary
          </h3>
          <p className="text-sm text-gray-700 leading-relaxed">{result.summary}</p>
        </div>
      )}

      {result.action_plan.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-indigo-700 uppercase tracking-wide mb-3">
            Action Plan
          </h3>
          <ol className="space-y-3">
            {result.action_plan.map((step) => (
              <li key={step.step} className="flex gap-3">
                <span className="flex-shrink-0 w-7 h-7 rounded-full bg-indigo-600 text-white text-xs font-bold flex items-center justify-center">
                  {step.step}
                </span>
                <div>
                  <p className="text-sm font-medium text-gray-800">{step.action}</p>
                  {step.rationale && (
                    <p className="text-xs text-gray-500 mt-0.5">{step.rationale}</p>
                  )}
                </div>
              </li>
            ))}
          </ol>
        </div>
      )}

      <p className="text-xs text-gray-400">
        Run ID: {result.id} · Started: {new Date(result.created_at).toLocaleString()}
        {result.completed_at && ` · Completed: ${new Date(result.completed_at).toLocaleString()}`}
      </p>
    </div>
  );
}
