"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";
import { Product, Sale } from "@/types";
import { SaleForm } from "@/components/sales/SaleForm";
import { Table } from "@/components/ui/Table";
import { Badge } from "@/components/ui/Badge";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { useAuth } from "@/lib/hooks/useAuth";

export default function SalesPage() {
  const { id } = useParams<{ id: string }>();
  const [sales, setSales] = useState<Sale[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [open, setOpen] = useState(false);
  const [salesError, setSalesError] = useState<string | null>(null);
  const [actionFeedback, setActionFeedback] = useState<{ type: "error" | "success"; message: string } | null>(null);
  const { userType, tokenPayload } = useAuth();
  const canManageSales = userType !== "commissioner" || (tokenPayload?.full_access ?? false);

  function parseErrorMessage(error: unknown, fallback = "Erro na operacao.") {
    if (!(error instanceof Error)) return fallback;
    try {
      const parsed = JSON.parse(error.message) as { detail?: string | { msg?: string }[] };
      if (typeof parsed.detail === "string") return parsed.detail;
      if (Array.isArray(parsed.detail) && parsed.detail.length > 0) {
        return parsed.detail[0]?.msg ?? fallback;
      }
      return fallback;
    } catch {
      return error.message || fallback;
    }
  }

  function formatDateTime(value?: string | null) {
    if (!value) return "-";
    return new Date(value).toLocaleString("pt-BR", {
      dateStyle: "short",
      timeStyle: "short",
    });
  }

  async function loadSales() {
    try {
      const salesData = await api.getSales(String(id));
      setSales(salesData);
      setSalesError(null);
    } catch (error) {
      // Keep UI usable and show actionable feedback instead of silent empty table.
      setSales([]);
      setSalesError(parseErrorMessage(error, "Nao foi possivel carregar as vendas deste evento."));
    }

    try {
      const productsData = await api.getProducts(String(id));
      setProducts(productsData);
    } catch {
      setProducts([]);
    }
  }

  useEffect(() => {
    loadSales();
  }, [id]);

  const summary = useMemo(() => {
    const paid = sales.filter((s) => s.status === "paid");
    const cancelled = sales.filter((s) => s.status === "cancelled");
    const checkin = sales.filter((s) => s.checkinAt || (s as { checkin_at?: string | null }).checkin_at);
    const revenue = paid.reduce((acc, item) => acc + item.price, 0);
    return { paid: paid.length, cancelled: cancelled.length, checkin: checkin.length, revenue };
  }, [sales]);

  return (
    <main style={{ display: "grid", gap: "1rem" }}>
      <section className="card" style={{ padding: "1rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1 style={{ margin: 0 }}>Vendas <Badge status="paid">{summary.paid} pagas</Badge></h1>
        </div>
        <Button onClick={() => setOpen(true)}>+ Vender ingresso</Button>
      </section>

      <section className="kpi-grid">
        <article className="card"><strong>Receita</strong><p>{new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(summary.revenue)}</p></article>
        <article className="card"><strong>Vendidas</strong><p>{summary.paid}</p></article>
        <article className="card"><strong>Canceladas</strong><p>{summary.cancelled}</p></article>
        <article className="card"><strong>Check-in</strong><p>{summary.checkin}</p></article>
      </section>

      {salesError ? <p className="inline-error">{salesError}</p> : null}
      {actionFeedback ? <p className={actionFeedback.type === "error" ? "inline-error" : "inline-success"}>{actionFeedback.message}</p> : null}

      <section className="card" style={{ padding: "1rem" }}>
        <Table>
          <thead>
            <tr>
              <th>Codigo</th><th>Comprador</th><th>Produto</th><th>Valor</th><th>Pagamento</th><th>Status</th><th>Data</th><th>Check-in</th><th>Acoes</th>
            </tr>
          </thead>
          <tbody>
            {sales.map((sale) => (
              <tr key={sale.id}>
                <td>{sale.code ?? sale.id}</td>
                <td>{sale.buyerName ?? (sale as { buyer_name?: string }).buyer_name}</td>
                <td>{sale.productId ?? (sale as { product_id?: string }).product_id}</td>
                <td>{new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(sale.price)}</td>
                <td>{sale.paymentMethod ?? (sale as { method_of_payment?: string }).method_of_payment}</td>
                <td><Badge status={sale.status} /></td>
                <td>{formatDateTime(sale.createdAt ?? (sale as { sale_date?: string }).sale_date ?? null)}</td>
                <td>{formatDateTime(sale.checkinAt ?? (sale as { checkin_at?: string }).checkin_at ?? null)}</td>
                <td style={{ display: "flex", gap: 6 }}>
                  {canManageSales && (
                    <>
                      <Button
                        type="button"
                        style={{ padding: "0.35rem 0.6rem", fontSize: "0.82rem" }}
                        onClick={async () => {
                          if (!window.confirm("Confirmar check-in desta venda?")) return;
                          try {
                            await api.checkinSale(String(id), String(sale.id));
                            setActionFeedback({ type: "success", message: "Check-in realizado com sucesso." });
                            await loadSales();
                          } catch (error) {
                            setActionFeedback({ type: "error", message: parseErrorMessage(error, "Nao foi possivel realizar o check-in.") });
                          }
                        }}
                      >
                        check-in
                      </Button>
                      <Button
                        type="button"
                        variant="danger"
                        style={{ padding: "0.35rem 0.6rem", fontSize: "0.82rem", background: "#fff5f5" }}
                        onClick={async () => {
                          if (!window.confirm("Confirmar cancelamento desta venda?")) return;
                          try {
                            await api.cancelSale(String(id), String(sale.id));
                            setActionFeedback({ type: "success", message: "Venda cancelada com sucesso." });
                            await loadSales();
                          } catch (error) {
                            setActionFeedback({ type: "error", message: parseErrorMessage(error, "Nao foi possivel cancelar a venda.") });
                          }
                        }}
                      >
                        cancelar
                      </Button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </section>

      <Modal open={open} title="Vender ingresso" onClose={() => setOpen(false)}>
        <SaleForm
          products={products}
          onSubmit={async (payload) => {
            await api.createSale(String(id), payload);
            setOpen(false);
            loadSales();
          }}
        />
      </Modal>
    </main>
  );
}
