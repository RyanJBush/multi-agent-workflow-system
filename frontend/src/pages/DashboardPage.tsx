import { useState } from "react";
import { AgentOutputCard } from "../components/AgentOutputCard";
import { FinalResultPanel } from "../components/FinalResultPanel";
import { HistoryList } from "../components/HistoryList";
import { WorkflowForm } from "../components/WorkflowForm";
import { useHistory } from "../hooks/useHistory";
import { useWorkflow } from "../hooks/useWorkflow";
import { api } from "../lib/api";
import type { WorkflowResponse } from "../types/workflow";

export function DashboardPage() {
  const { status, result, error, run, reset } = useWorkflow();
  const { history, loading: histLoading, error: histError, refresh } = useHistory();
  const [selectedRun, setSelectedRun] = useState<WorkflowResponse | null>(null);

  const handleRunWorkflow = async (task: string) => {
    reset();
    setSelectedRun(null);
    await run(task);
    refresh();
  };

  const handleSelectHistory = async (id: string) => {
    try {
      const run = await api.getWorkflow(id);
      setSelectedRun(run);
      reset();
    } catch {
      // ignore
    }
  };

  const activeResult = result ?? selectedRun;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-gray-900">Multi-Agent Workflow System</h1>
            <p className="text-xs text-gray-500 mt-0.5">
              Research → Summarizer → Planner pipeline
            </p>
          </div>
          <span className="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium">
            ● Live
          </span>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left column */}
        <div className="lg:col-span-1 space-y-8">
          {/* Workflow submission form */}
          <section className="bg-white rounded-xl border border-gray-200 p-6">
            <h2 className="text-base font-semibold text-gray-800 mb-4">Submit a Task</h2>
            <WorkflowForm onSubmit={handleRunWorkflow} isLoading={status === "loading"} />
            {error && (
              <div className="mt-4 rounded-lg bg-red-50 border border-red-200 px-4 py-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}
          </section>

          {/* History */}
          <section className="bg-white rounded-xl border border-gray-200 p-6">
            <HistoryList
              history={history}
              loading={histLoading}
              error={histError}
              onSelect={handleSelectHistory}
              onRefresh={refresh}
            />
          </section>
        </div>

        {/* Right column */}
        <div className="lg:col-span-2 space-y-6">
          {/* Loading state */}
          {status === "loading" && (
            <div className="rounded-xl border border-gray-200 bg-white p-10 flex flex-col items-center justify-center gap-3">
              <div className="w-10 h-10 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin" />
              <p className="text-sm text-gray-500">Running agents… this may take a moment.</p>
            </div>
          )}

          {/* Agent outputs */}
          {activeResult && activeResult.agent_results.length > 0 && (
            <div className="space-y-4">
              <h2 className="text-base font-semibold text-gray-800">Agent Outputs</h2>
              {activeResult.agent_results.map((r) => (
                <AgentOutputCard key={r.agent_name} result={r} />
              ))}
            </div>
          )}

          {/* Final result */}
          {activeResult && <FinalResultPanel result={activeResult} />}

          {/* Empty state */}
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
