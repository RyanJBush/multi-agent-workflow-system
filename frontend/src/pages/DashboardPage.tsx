import { useEffect } from 'react'

import AgentOutputPanel from '../components/AgentOutputPanel'
import FinalResultPanel from '../components/FinalResultPanel'
import HistoryList from '../components/HistoryList'
import WorkflowForm from '../components/WorkflowForm'
import { useWorkflow } from '../hooks/useWorkflow'

export default function DashboardPage() {
  const { result, history, loading, error, submitWorkflow, loadHistory, loadRunDetail } = useWorkflow()

  useEffect(() => {
    void loadHistory()
  }, [])

  return (
    <main className="min-h-screen bg-slate-100 p-6 text-slate-900 md:p-10">
      <div className="mx-auto grid max-w-7xl gap-6 lg:grid-cols-[1.2fr,0.8fr]">
        <section className="space-y-6">
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h1 className="text-xl font-semibold">Multi-Agent Workflow Dashboard</h1>
            <p className="mt-1 text-sm text-slate-600">
              Submit a workflow request and inspect outputs from each specialized agent.
            </p>
            <div className="mt-5">
              <WorkflowForm isSubmitting={loading} onSubmit={submitWorkflow} />
            </div>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold">Final Result</h2>
            <div className="mt-4">
              <FinalResultPanel result={result} />
            </div>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold">Per-Agent Outputs</h2>
            <div className="mt-4">
              <AgentOutputPanel agentResults={result?.agent_results ?? []} />
            </div>
          </div>
        </section>

        <aside className="space-y-6">
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold">Workflow History</h2>
            <div className="mt-4">
              <HistoryList items={history} onSelect={loadRunDetail} />
            </div>
          </div>

          {error && (
            <div className="rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">
              {error}
            </div>
          )}
        </aside>
      </div>
    </main>
  )
}
