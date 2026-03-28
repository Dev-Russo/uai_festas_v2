"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { DashboardData } from "@/types";

export function useDashboard(eventId: string) {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!eventId) {
      return;
    }

    api
      .getEventDashboard(eventId)
      .then((result) => setData(result))
      .catch((err) => setError(err instanceof Error ? err.message : "Erro ao carregar dashboard"))
      .finally(() => setLoading(false));
  }, [eventId]);

  return { data, loading, error };
}
