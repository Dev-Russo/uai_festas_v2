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

export default function SalesPage() {
  const { id } = useParams<{ id: string }>();
  const [sales, setSales] = useState<Sale[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [open, setOpen] = useState(false);

  async function loadSales() {
    const [salesData, productsData] = await Promise.all([api.getSales(String(id)), api.getProducts(String(id))]);
    setSales(salesData);
    setProducts(productsData);
  }

  useEffect(() => {
    Promise.all([api.getSales(String(id)), api.getProducts(String(id))])
      .then(([salesData, productsData]) => {
        setSales(salesData);
        setProducts(productsData);
      })
      .catch(() => {
        setSales([]);
        setProducts([]);
      });
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
        <Button onClick={() => setOpen(true)}>+ Registrar Venda</Button>
      </section>

      <section className="kpi-grid">
        <article className="card"><strong>Receita</strong><p>{new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(summary.revenue)}</p></article>
        <article className="card"><strong>Vendidas</strong><p>{summary.paid}</p></article>
        <article className="card"><strong>Canceladas</strong><p>{summary.cancelled}</p></article>
        <article className="card"><strong>Check-in</strong><p>{summary.checkin}</p></article>
      </section>

      <section className="card" style={{ padding: "1rem" }}>
        <Table>
          <thead>
            <tr>
              <th>Codigo</th><th>Comprador</th><th>Produto</th><th>Valor</th><th>Pagamento</th><th>Status</th><th>Data</th><th>Acoes</th>
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
                <td>{(sale.createdAt ?? (sale as { sale_date?: string }).sale_date) ? new Date((sale.createdAt ?? (sale as { sale_date?: string }).sale_date) as string).toLocaleDateString("pt-BR") : "-"}</td>
                <td style={{ display: "flex", gap: 6 }}>
                  <button className="button-ghost" type="button" onClick={async () => {
                    await api.checkinSale(String(id), String(sale.id));
                    loadSales();
                  }}>check-in</button>
                  <button className="button-ghost" type="button" onClick={async () => {
                    await api.cancelSale(String(id), String(sale.id));
                    loadSales();
                  }}>cancelar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </section>

      <Modal open={open} title="Registrar venda" onClose={() => setOpen(false)}>
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
