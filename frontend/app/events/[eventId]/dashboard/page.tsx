"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { SideMenu } from "../../../components/side-menu";
import { clearToken, getToken } from "../../../lib/auth";
import { DashboardResponse, getDashboard, getEventById } from "../../../lib/api";

type ActivePanel = "dashboard" | "products" | "sales";

export default function EventDashboardPage() {
  const params = useParams<{ eventId: string }>();
  const router = useRouter();
  const eventId = params?.eventId ?? "";

  const [activePanel, setActivePanel] = useState<ActivePanel>("dashboard");
  const [eventName, setEventName] = useState("Evento");
  const [dashboard, setDashboard] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.replace("/");
      return;
    }
    const authToken = token;

    async function loadData() {
      try {
        const [eventData, dashboardData] = await Promise.all([
          getEventById(eventId, authToken),
          getDashboard(eventId, authToken),
        ]);
        setEventName(eventData.name);
        setDashboard(dashboardData);
      } catch (err) {
        const message = err instanceof Error ? err.message : "Nao foi possivel carregar o dashboard.";
        setError(message);
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [eventId, router]);

  const maxProductSales = useMemo(() => {
    if (!dashboard?.sales_by_product.length) {
      return 1;
    }
    return Math.max(...dashboard.sales_by_product.map((item) => item.sales_count), 1);
  }, [dashboard]);

  const maxDailySales = useMemo(() => {
    if (!dashboard?.sales_by_day.length) {
      return 1;
    }
    return Math.max(...dashboard.sales_by_day.map((item) => item.sales_count), 1);
  }, [dashboard]);

  function handleLogout() {
    clearToken();
    router.push("/");
  }

  return (
    <main className="page-shell" style={{ display: "grid", gap: "1rem" }}>
      <header className="card" style={{ padding: "1rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <p style={{ margin: 0, fontFamily: "var(--font-plex-mono)", color: "var(--app-accent-strong)", fontSize: "0.8rem" }}>
            PAINEL DO EVENTO
          </p>
          <h1 style={{ margin: "0.25rem 0 0" }}>{eventName}</h1>
        </div>
        <button className="button-ghost" type="button" onClick={() => router.push("/events")}>Voltar para Meus Eventos</button>
      </header>

      <section
        className="grid grid-cols-1 xl:grid-cols-[280px_1fr]"
        style={{
          gap: "1rem",
          alignItems: "start",
        }}
      >
        <SideMenu active={activePanel} onSelect={setActivePanel} eventName={eventName} onLogout={handleLogout} />

        <div className="card" style={{ padding: "1rem", minHeight: 500 }}>
          {loading ? <p className="muted">Carregando dados do dashboard...</p> : null}
          {!loading && error ? <p style={{ color: "var(--app-danger)" }}>{error}</p> : null}

          {!loading && !error && activePanel === "products" ? (
            <div>
              <h2 style={{ marginTop: 0 }}>Produtos</h2>
              <p className="muted">Pagina de produtos entra na proxima etapa. O menu ja esta ativo e integrado.</p>
            </div>
          ) : null}

          {!loading && !error && activePanel === "sales" ? (
            <div>
              <h2 style={{ marginTop: 0 }}>Vendas</h2>
              <p className="muted">Pagina de vendas entra na proxima etapa. O menu ja esta ativo e integrado.</p>
            </div>
          ) : null}

          {!loading && !error && activePanel === "dashboard" && dashboard ? (
            <div style={{ display: "grid", gap: "1rem" }}>
              <section className="stat-grid">
                <article className="card" style={{ padding: "0.9rem", background: "var(--app-surface)" }}>
                  <p className="muted" style={{ margin: 0 }}>Vendas pagas</p>
                  <strong style={{ fontSize: "1.6rem" }}>{dashboard.total_paid_sales}</strong>
                </article>
                <article className="card" style={{ padding: "0.9rem", background: "var(--app-surface)" }}>
                  <p className="muted" style={{ margin: 0 }}>Vendas canceladas</p>
                  <strong style={{ fontSize: "1.6rem" }}>{dashboard.total_canceled_sales}</strong>
                </article>
                <article className="card" style={{ padding: "0.9rem", background: "var(--app-surface)" }}>
                  <p className="muted" style={{ margin: 0 }}>Receita total</p>
                  <strong style={{ fontSize: "1.6rem" }}>R$ {dashboard.total_revenue.toFixed(2)}</strong>
                </article>
                <article className="card" style={{ padding: "0.9rem", background: "var(--app-surface)" }}>
                  <p className="muted" style={{ margin: 0 }}>Ticket medio</p>
                  <strong style={{ fontSize: "1.6rem" }}>R$ {dashboard.average_ticket.toFixed(2)}</strong>
                </article>
              </section>

              <section className="card" style={{ padding: "1rem", background: "var(--app-surface)" }}>
                <h3 style={{ marginTop: 0 }}>Vendas por produto</h3>
                {dashboard.sales_by_product.length === 0 ? (
                  <p className="muted">Sem vendas por produto ainda.</p>
                ) : (
                  <div style={{ display: "grid", gap: "0.7rem" }}>
                    {dashboard.sales_by_product.map((item) => (
                      <div key={item.product_name} className="bar-row">
                        <span style={{ fontSize: "0.88rem" }}>{item.product_name}</span>
                        <div className="bar-track">
                          <div
                            className="bar-fill"
                            style={{ width: `${Math.max((item.sales_count / maxProductSales) * 100, 6)}%` }}
                          />
                        </div>
                        <strong style={{ textAlign: "right", fontSize: "0.85rem" }}>{item.sales_count}</strong>
                      </div>
                    ))}
                  </div>
                )}
              </section>

              <section className="card" style={{ padding: "1rem", background: "var(--app-surface)" }}>
                <h3 style={{ marginTop: 0 }}>Vendas por dia (ultimos 30 dias)</h3>
                {dashboard.sales_by_day.length === 0 ? (
                  <p className="muted">Sem vendas por dia ainda.</p>
                ) : (
                  <div style={{ display: "grid", gap: "0.7rem" }}>
                    {dashboard.sales_by_day.map((item) => (
                      <div key={item.sale_date} className="bar-row">
                        <span style={{ fontSize: "0.88rem" }}>
                          {new Date(item.sale_date).toLocaleDateString("pt-BR")}
                        </span>
                        <div className="bar-track">
                          <div
                            className="bar-fill"
                            style={{ width: `${Math.max((item.sales_count / maxDailySales) * 100, 6)}%` }}
                          />
                        </div>
                        <strong style={{ textAlign: "right", fontSize: "0.85rem" }}>{item.sales_count}</strong>
                      </div>
                    ))}
                  </div>
                )}
              </section>

              <section className="card" style={{ padding: "1rem", background: "var(--app-surface)" }}>
                <h3 style={{ marginTop: 0 }}>Taxa de cancelamento</h3>
                <p style={{ marginBottom: 0, fontSize: "1.3rem", fontWeight: 700 }}>
                  {(dashboard.cancellation_rate * 100).toFixed(1)}%
                </p>
              </section>
            </div>
          ) : null}
        </div>
      </section>
    </main>
  );
}
