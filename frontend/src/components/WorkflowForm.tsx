import { useState } from "react";

interface Props {
  onSubmit: (task: string) => Promise<void> | void;
  isLoading: boolean;
}

const MIN_TASK_LEN = 5;
const MAX_TASK_LEN = 2000;

export function WorkflowForm({ onSubmit, isLoading }: Props) {
  const [task, setTask] = useState("");

  const isValid = task.trim().length >= MIN_TASK_LEN;

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!isValid || isLoading) return;
    await onSubmit(task.trim());
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="task" className="block text-sm font-semibold text-gray-700 mb-1">
          Research or Planning Task
        </label>
        <textarea
          id="task"
          name="task"
          rows={5}
          required
          minLength={MIN_TASK_LEN}
          maxLength={MAX_TASK_LEN}
          value={task}
          onChange={(e) => setTask(e.target.value)}
          placeholder="e.g. Research the impact of AI on healthcare in 2024 and produce an action plan."
          className="w-full rounded-lg border border-gray-300 px-4 py-3 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-200 resize-none"
          disabled={isLoading}
        />
        <div className="mt-1 flex items-center justify-between text-xs">
          <span className={isValid ? "text-emerald-600" : "text-gray-400"}>
            Minimum {MIN_TASK_LEN} characters
          </span>
          <span className="text-gray-400">
            {task.length}/{MAX_TASK_LEN}
          </span>
        </div>
      </div>
      <button
        type="submit"
        disabled={isLoading || !isValid}
        className="w-full rounded-lg bg-indigo-600 px-6 py-3 text-sm font-semibold text-white shadow hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {isLoading ? "Running workflow…" : "Run Workflow"}
      </button>
    </form>
  );
}
