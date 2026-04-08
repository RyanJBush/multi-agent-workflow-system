import { useState } from "react";
import { AgentOutputCard } from "../components/AgentOutputCard";
import { FinalResultPanel } from "../components/FinalResultPanel";
import { HistoryList } from "../components/HistoryList";
import { WorkflowDetailHeader } from "../components/WorkflowDetailHeader";
import { WorkflowForm } from "../components/WorkflowForm";
import { useHistory } from "../hooks/useHistory";
import { useWorkflow } from "../hooks/useWorkflow";
import { api } from "../lib/api";
import type { WorkflowResponse } from "../types/workflow";

type ViewSource = "current" | "history";

export function DashboardPage() {
  const { status, result, error, run, reset } = useWorkflow();
  const { history, loading: histLoading, error: histError, refresh } = useHistory();
  const [selectedRun, setSelectedRun] = useState<WorkflowResponse | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detailLoadError, setDetailLoadError] = useState<string | null>(null);

  const handleRunWorkflow = async (task: string) => {
    setDetailLoadError(null);
    setSelectedRun(null);
    setSelectedId(null);
    await run(task);
    await refresh();
  };

  const handleSelectHistory = async (id: string) => {
    setDetailLoadError(null);
    setSelectedId(id);
    try {
      const run = await api.getWorkflow(id);
      setSelectedRun(run);
      reset();
    } catch (err) {
      setDetailLoadError(err instanceof Error ? err.message : "Unable to load workflow details.");
    }
  };

  const activeResult = result ?? selectedRun;
  const source: ViewSource = result ? "current" : "history";

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-gray-900">Multi-Agent Workflow System</h1>
            <p className="text-xs text-gray-500 mt-0.5">Research → Summarizer → Planner pipeline</p>
          </div>
          <span className="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium">
            ● Live
          </span>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1 space-y-8">
          <section className="bg-white rounded-xl border border-gray-200 p-6">
            <h2 className="text-base font-semibold text-gray-800 mb-4">Submit a Task</h2>
            <WorkflowForm onSubmit={handleRunWorkflow} isLoading={status === "loading"} />
            {error && (
              <div className="mt-4 rounded-lg bg-red-50 border border-red-200 px-4 py-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}
          </section>

          <section className="bg-white rounded-xl border border-gray-200 p-6">
            <HistoryList
              history={history}
              loading={histLoading}
              error={histError}
              selectedId={selectedId}
              onSelect={handleSelectHistory}
              onRefresh={refresh}
            />
          </section>
        </div>

        <div className="lg:col-span-2 space-y-6">
          {detailLoadError && (
            <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
              {detailLoadError}
            </div>
          )}

          {status === "loading" && (
            <div className="rounded-xl border border-gray-200 bg-white p-10 flex flex-col items-center justify-center gap-3">
              <div className="w-10 h-10 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
              <p className="text-sm text-gray-500">Running agents… this may take a moment.</p>
            </div>
          )}

          {activeResult && <WorkflowDetailHeader result={activeResult} source={source} />}

          {activeResult && activeResult.agent_results.length > 0 && (
            <div className="space-y-4">
              <h2 className="text-base font-semibold text-gray-800">Agent Outputs</h2>
              {activeResult.agent_results.map((r) => (
                <AgentOutputCard key={r.agent_name} result={r} />
              ))}
            </div>
          )}

          {activeResult && <FinalResultPanel result={activeResult} />}

          {status === "idle" && !activeResult && (
            <div className="rounded-xl border border-dashed border-gray-300 bg-white p-12 flex flex-col items-center justify-center text-center">
              <p className="text-4xl mb-3">🤖</p>
              <p className="text-gray-500 text-sm">
                Submit a task to start the multi-agent workflow.
              </p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
