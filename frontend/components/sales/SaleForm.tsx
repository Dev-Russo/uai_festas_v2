"use client";

import { FormEvent, useState } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { CreateSaleDTO, PaymentMethod, Product } from "@/types";

export function SaleForm({
  products,
  onSubmit,
}: {
  products: Product[];
  onSubmit: (payload: CreateSaleDTO) => Promise<void>;
}) {
  const [payload, setPayload] = useState<CreateSaleDTO>({
    productId: "",
    buyerName: "",
    buyerEmail: "",
    paymentMethod: "pix",
  });

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    await onSubmit(payload);
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: "grid", gap: "0.6rem" }}>
      <label style={{ display: "grid", gap: "0.35rem" }}>
        <span style={{ fontSize: "0.9rem", color: "var(--text-secondary)" }}>Produto</span>
        <select
          className="input-field"
          value={payload.productId}
          onChange={(e) => {
            setPayload((prev) => ({ ...prev, productId: e.target.value }));
          }}
        >
          <option value="">Selecione</option>
          {products.map((product) => {
            const soldOut = product.quantity != null && product.quantity <= 0;
            const stockLabel = product.quantity == null
              ? "ilimitado"
              : soldOut
              ? "esgotado"
              : `${product.quantity} restantes`;
            return (
              <option key={product.id} value={String(product.id)} disabled={soldOut}>
                {product.name} · {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(product.price)} · {stockLabel}
              </option>
            );
          })}
        </select>
      </label>
      {products.length === 0 ? <small className="muted">Nenhum lote disponivel para este evento.</small> : null}
      <Input label="Comprador" value={payload.buyerName} onChange={(e) => setPayload((v) => ({ ...v, buyerName: e.target.value }))} />
      <Input label="Email" type="email" value={payload.buyerEmail} onChange={(e) => setPayload((v) => ({ ...v, buyerEmail: e.target.value }))} />
      <label style={{ display: "grid", gap: "0.35rem" }}>
        <span style={{ fontSize: "0.9rem", color: "var(--text-secondary)" }}>Pagamento</span>
        <select
          className="input-field"
          value={payload.paymentMethod}
          onChange={(e) => setPayload((v) => ({ ...v, paymentMethod: e.target.value as PaymentMethod }))}
        >
          <option value="pix">PIX</option>
          <option value="credit_card">Credito</option>
          <option value="debit_card">Debito</option>
          <option value="cash">Dinheiro</option>
        </select>
      </label>
      <Button type="submit" disabled={!payload.productId || products.length === 0}>Vender ingresso</Button>
    </form>
  );
}
