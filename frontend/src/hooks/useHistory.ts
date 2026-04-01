import { useEffect, useState } from "react";
import { api } from "../lib/api";
import type { WorkflowSummary } from "../types/workflow";

export function useHistory() {
  const [history, setHistory] = useState<WorkflowSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetch = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getHistory();
      setHistory(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetch();
  }, []);

  return { history, loading, error, refresh: fetch };
}
