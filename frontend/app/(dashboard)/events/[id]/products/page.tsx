"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";
import { Product } from "@/types";
import { ProductForm } from "@/components/products/ProductForm";
import { Table } from "@/components/ui/Table";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";

export default function ProductsPage() {
  const { id } = useParams<{ id: string }>();
  const [products, setProducts] = useState<Product[]>([]);
  const [open, setOpen] = useState(false);

  async function loadProducts() {
    const data = await api.getProducts(String(id));
    setProducts(data);
  }

  useEffect(() => {
    api
      .getProducts(String(id))
      .then((data) => setProducts(data))
      .catch(() => setProducts([]));
  }, [id]);

  return (
    <main style={{ display: "grid", gap: "1rem" }}>
      <section className="card" style={{ padding: "1rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <p className="muted" style={{ margin: 0 }}>Eventos &gt; {id} &gt; Lotes</p>
          <h1 style={{ margin: "0.35rem 0 0" }}>Lotes de Ingresso</h1>
        </div>
        <Button onClick={() => setOpen(true)}>+ Novo Lote</Button>
      </section>

      <section className="card" style={{ padding: "1rem" }}>
        <Table>
          <thead>
            <tr>
              <th>Nome</th><th>Preco</th><th>Qtd. Total</th><th>Disponivel</th><th>Periodo</th><th>Acoes</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr key={product.id}>
                <td>{product.name}</td>
                <td>{new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(product.price)}</td>
                <td>{product.quantity ?? "-"}</td>
                <td>{product.quantity ?? "-"}</td>
                <td>-</td>
                <td>
                  <button className="button-ghost" type="button">Editar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </section>

      <Modal open={open} title="Novo lote" onClose={() => setOpen(false)}>
        <ProductForm
          onSubmit={async (payload) => {
            await api.createProduct(String(id), payload);
            setOpen(false);
            loadProducts();
          }}
        />
      </Modal>
    </main>
  );
}
