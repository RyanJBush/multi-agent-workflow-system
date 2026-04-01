interface Props {
  onSubmit: (task: string) => void;
  isLoading: boolean;
}

export function WorkflowForm({ onSubmit, isLoading }: Props) {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const task = (fd.get("task") as string).trim();
    if (task.length >= 5) onSubmit(task);
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
          rows={4}
          required
          minLength={5}
          maxLength={2000}
          placeholder="e.g. Research the impact of AI on healthcare in 2024 and produce an action plan."
          className="w-full rounded-lg border border-gray-300 px-4 py-3 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-200 resize-none"
          disabled={isLoading}
        />
      </div>
      <button
        type="submit"
        disabled={isLoading}
        className="w-full rounded-lg bg-indigo-600 px-6 py-3 text-sm font-semibold text-white shadow hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {isLoading ? "Running workflow…" : "Run Workflow"}
      </button>
    </form>
  );
}
