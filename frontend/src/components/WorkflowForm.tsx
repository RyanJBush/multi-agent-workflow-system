import { useState } from 'react'

import type { WorkflowRequest } from '../types/workflow'

interface WorkflowFormProps {
  isSubmitting: boolean
  onSubmit: (payload: WorkflowRequest) => void
}

export default function WorkflowForm({ isSubmitting, onSubmit }: WorkflowFormProps) {
  const [title, setTitle] = useState('US campus productivity app research')
  const [objective, setObjective] = useState(
    'Identify a practical go-to-market approach for first 90 days with limited budget.',
  )
  const [constraints, setConstraints] = useState('low budget, small team')
  const [audience, setAudience] = useState('student founders')
  const [outputFormat, setOutputFormat] = useState<'action_plan' | 'brief' | 'both'>('both')

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    onSubmit({
      title,
      objective,
      constraints: constraints
        .split(',')
        .map((item) => item.trim())
        .filter(Boolean),
      audience,
      output_format: outputFormat,
    })
  }

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      <div>
        <label className="mb-1 block text-sm font-medium text-slate-700">Task Title</label>
        <input
          className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          required
        />
      </div>

      <div>
        <label className="mb-1 block text-sm font-medium text-slate-700">Objective</label>
        <textarea
          className="h-28 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
          value={objective}
          onChange={(event) => setObjective(event.target.value)}
          required
        />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <label className="mb-1 block text-sm font-medium text-slate-700">Constraints (comma-separated)</label>
          <input
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
            value={constraints}
            onChange={(event) => setConstraints(event.target.value)}
          />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-slate-700">Audience</label>
          <input
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
            value={audience}
            onChange={(event) => setAudience(event.target.value)}
          />
        </div>
      </div>

      <div>
        <label className="mb-1 block text-sm font-medium text-slate-700">Output Format</label>
        <select
          className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
          value={outputFormat}
          onChange={(event) =>
            setOutputFormat(event.target.value as 'action_plan' | 'brief' | 'both')
          }
        >
          <option value="both">Summary + Action Plan</option>
          <option value="brief">Summary Only</option>
          <option value="action_plan">Action Plan Only</option>
        </select>
      </div>

      <button
        className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
        disabled={isSubmitting}
        type="submit"
      >
        {isSubmitting ? 'Running Workflow...' : 'Run Workflow'}
      </button>
    </form>
  )
}
