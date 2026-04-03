import { useState } from 'react'

import { fetchWorkflowHistory, fetchWorkflowRun, runWorkflow } from '../lib/api'
import type { WorkflowRequest, WorkflowResult, WorkflowRunRecord } from '../types/workflow'

export function useWorkflow() {
  const [result, setResult] = useState<WorkflowResult | null>(null)
  const [history, setHistory] = useState<WorkflowRunRecord[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function loadHistory() {
    try {
      const data = await fetchWorkflowHistory(20)
      setHistory(data.items)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load workflow history.'
      setError(message)
    }
  }

  async function submitWorkflow(payload: WorkflowRequest) {
    setLoading(true)
    setError(null)

    try {
      const data = await runWorkflow(payload)
      setResult(data)
      await loadHistory()
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Workflow run failed. Please try again.'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  async function loadRunDetail(runId: string) {
    setLoading(true)
    setError(null)

    try {
      const data = await fetchWorkflowRun(runId)
      setResult(data.response_payload)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load workflow run detail.'
      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return {
    result,
    history,
    loading,
    error,
    submitWorkflow,
    loadHistory,
    loadRunDetail,
  }
}
