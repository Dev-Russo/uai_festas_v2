"use client";

import { FormEvent, useMemo, useState } from "react";
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
    price: 0,
  });

  const selectedProduct = useMemo(() => products.find((p) => String(p.id) === payload.productId), [payload.productId, products]);

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
            const product = products.find((item) => String(item.id) === e.target.value);
            setPayload((prev) => ({ ...prev, productId: e.target.value, price: product?.price ?? 0 }));
          }}
        >
          <option value="">Selecione</option>
          {products.map((product) => (
            <option key={product.id} value={String(product.id)}>{product.name}</option>
          ))}
        </select>
      </label>
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
      <Input
        label="Valor"
        type="number"
        value={String(payload.price)}
        onChange={(e) => setPayload((v) => ({ ...v, price: Number(e.target.value) }))}
      />
      {selectedProduct ? <small className="muted">Valor sugerido pelo lote: R$ {selectedProduct.price}</small> : null}
      <Button type="submit">Registrar venda</Button>
    </form>
  );
}
