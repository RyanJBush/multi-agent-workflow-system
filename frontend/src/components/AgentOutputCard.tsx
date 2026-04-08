import type { AgentResult, PlanOutput, ResearchFindings, SummaryOutput } from "../types/workflow";

const AGENT_LABELS: Record<string, string> = {
  research: "🔍 Research Agent",
  summarizer: "📝 Summarizer Agent",
  planner: "🗺️ Planner Agent",
};

function ResearchCard({ data }: { data: ResearchFindings }) {
  return (
    <div className="space-y-3">
      <div>
        <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
          Key Facts
        </p>
        <ul className="list-disc pl-5 space-y-1">
          {data.key_facts.map((f, i) => (
            <li key={i} className="text-sm text-gray-700">
              {f}
            </li>
          ))}
        </ul>
      </div>
      {data.gaps.length > 0 && (
        <div>
          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Gaps</p>
          <ul className="list-disc pl-5 space-y-1">
            {data.gaps.map((g, i) => (
              <li key={i} className="text-sm text-gray-500 italic">
                {g}
              </li>
            ))}
          </ul>
        </div>
      )}
      {data.sources.length > 0 && (
        <div>
          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
            Sources
          </p>
          <p className="text-sm text-gray-600">{data.sources.join(", ")}</p>
        </div>
      )}
    </div>
  );
}

function SummaryCard({ data }: { data: SummaryOutput }) {
  return (
    <p className="text-sm text-gray-700 leading-relaxed">
      {data.summary} <span className="text-xs text-gray-400">({data.word_count} words)</span>
    </p>
  );
}

function PlanCard({ data }: { data: PlanOutput }) {
  return (
    <ol className="space-y-2">
      {data.steps.map((s) => (
        <li key={s.step} className="flex gap-3">
          <span className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-100 text-indigo-700 text-xs font-bold flex items-center justify-center">
            {s.step}
          </span>
          <div>
            <p className="text-sm font-medium text-gray-800">{s.action}</p>
            {s.rationale && <p className="text-xs text-gray-500 mt-0.5">{s.rationale}</p>}
          </div>
        </li>
      ))}
    </ol>
  );
}

function renderOutput(agent_name: string, output: AgentResult["output"]) {
  if (!output) return <p className="text-sm text-gray-400">No output</p>;
  if (agent_name === "research") return <ResearchCard data={output as ResearchFindings} />;
  if (agent_name === "summarizer") return <SummaryCard data={output as SummaryOutput} />;
  if (agent_name === "planner") return <PlanCard data={output as PlanOutput} />;
  return (
    <pre className="text-xs text-gray-600 overflow-x-auto">{JSON.stringify(output, null, 2)}</pre>
  );
}

interface Props {
  result: AgentResult;
}

export function AgentOutputCard({ result }: Props) {
  const label = AGENT_LABELS[result.agent_name] ?? result.agent_name;
  const isSuccess = result.status === "success";

  return (
    <div
      className={`rounded-xl border p-5 ${isSuccess ? "border-gray-200 bg-white" : "border-red-200 bg-red-50"}`}
    >
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-gray-800">{label}</h3>
        <div className="flex items-center gap-2">
          <span
            className={`text-xs font-medium px-2 py-0.5 rounded-full ${
              isSuccess ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
            }`}
          >
            {result.status}
          </span>
          <span className="text-xs text-gray-400">{result.duration_ms}ms</span>
        </div>
      </div>
      {isSuccess ? (
        renderOutput(result.agent_name, result.output)
      ) : (
        <p className="text-sm text-red-600">{result.error}</p>
      )}
    </div>
  );
}
