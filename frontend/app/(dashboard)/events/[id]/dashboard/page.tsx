"use client";

import { useMemo } from "react";
import { useParams } from "next/navigation";
import { BarChart3, CircleDollarSign, TicketCheck, TrendingUp } from "lucide-react";
import { CancellationGauge } from "@/components/charts/CancellationGauge";
import { RevenueChart } from "@/components/charts/RevenueChart";
import { SalesByDayChart } from "@/components/charts/SalesByDayChart";
import { SalesByProductChart } from "@/components/charts/SalesByProductChart";
import { useDashboard } from "@/lib/hooks/useDashboard";

export default function EventDashboardPage() {
  const { id } = useParams<{ id: string }>();
  const { data, loading, error } = useDashboard(String(id));

  const salesByDay = useMemo(() => {
    return (data?.salesByDay ?? []).map((item) => ({
      ...item,
      date: new Date(item.date).toLocaleDateString("pt-BR"),
    }));
  }, [data]);

  return (
    <main style={{ display: "grid", gap: "1rem" }}>
      <section className="kpi-grid">
        <article className="card kpi-card"><CircleDollarSign size={18} /><small>Receita Total</small><strong>R$ {data?.totalRevenue.toFixed(2) ?? "0.00"}</strong></article>
        <article className="card kpi-card"><TrendingUp size={18} /><small>Ticket Medio</small><strong>R$ {data?.averageTicket.toFixed(2) ?? "0.00"}</strong></article>
        <article className="card kpi-card"><TicketCheck size={18} /><small>Vendas Pagas</small><strong>{data?.totalPaidSales ?? 0}</strong></article>
        <article className="card kpi-card"><BarChart3 size={18} /><small>Cancelamentos</small><strong>{data?.totalCancelledSales ?? 0}</strong></article>
      </section>

      {loading ? <p className="muted">Carregando dashboard...</p> : null}
      {error ? <p className="inline-error">{error}</p> : null}

      {!loading && data ? (
        <>
          <section className="chart-grid-main">
            <article className="card" style={{ padding: "1rem" }}>
              <h3 style={{ marginTop: 0 }}>Vendas por dia</h3>
              <RevenueChart data={salesByDay} />
            </article>
            <article className="card" style={{ padding: "1rem" }}>
              <h3 style={{ marginTop: 0 }}>Taxa de cancelamento</h3>
              <CancellationGauge rate={data.cancellationRate} />
            </article>
          </section>

          <section className="chart-grid-main">
            <article className="card" style={{ padding: "1rem" }}>
              <h3 style={{ marginTop: 0 }}>Ranking de produtos</h3>
              <SalesByProductChart data={data.salesByProduct} />
            </article>
            <article className="card" style={{ padding: "1rem" }}>
              <h3 style={{ marginTop: 0 }}>Distribuicao temporal</h3>
              <SalesByDayChart data={salesByDay} />
            </article>
          </section>
        </>
      ) : null}
    </main>
  );
}
