import type { WorkflowResponse } from "../types/workflow";

interface Props {
  result: WorkflowResponse;
  source: "current" | "history";
}

export function WorkflowDetailHeader({ result, source }: Props) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white px-5 py-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-wide text-gray-500 font-semibold">
            Workflow Detail
          </p>
          <h2 className="text-base font-semibold text-gray-900 mt-0.5">
            {source === "current" ? "Latest Run" : "History Selection"}
          </h2>
        </div>
        <span className="text-xs text-gray-500">ID: {result.id}</span>
      </div>
      <p className="mt-3 text-sm text-gray-700 line-clamp-2">{result.task}</p>
    </div>
  );
}
