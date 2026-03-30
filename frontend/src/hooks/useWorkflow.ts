import { useState } from "react";
import { api } from "../lib/api";
import type { WorkflowResponse } from "../types/workflow";

type Status = "idle" | "loading" | "success" | "error";

export function useWorkflow() {
  const [status, setStatus] = useState<Status>("idle");
  const [result, setResult] = useState<WorkflowResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const run = async (task: string) => {
    setStatus("loading");
    setError(null);
    setResult(null);
    try {
      const data = await api.runWorkflow({ task });
      setResult(data);
      setStatus("success");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      setStatus("error");
    }
  };

  const reset = () => {
    setStatus("idle");
    setResult(null);
    setError(null);
  };

  return { status, result, error, run, reset };
}
