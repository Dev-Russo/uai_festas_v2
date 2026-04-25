"use client";

import { FormEvent, useState } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { CreateProductDTO } from "@/types";

function toDatetimeLocal(iso?: string): string {
  if (!iso) return "";
  const d = new Date(iso);
  if (isNaN(d.getTime())) return "";
  return d.toISOString().slice(0, 16);
}

export function ProductForm({
  onSubmit,
  initialValues,
}: {
  onSubmit: (payload: CreateProductDTO) => Promise<void>;
  initialValues?: Partial<CreateProductDTO>;
}) {
  const [payload, setPayload] = useState<CreateProductDTO>({
    name: initialValues?.name ?? "",
    price: initialValues?.price ?? 0,
    quantity: initialValues?.quantity ?? 0,
    startDate: initialValues?.startDate ? toDatetimeLocal(initialValues.startDate) : "",
    endDate: initialValues?.endDate ? toDatetimeLocal(initialValues.endDate) : "",
  });

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    await onSubmit(payload);
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: "grid", gap: "0.6rem" }}>
      <Input label="Nome do lote" value={payload.name} onChange={(e) => setPayload((v) => ({ ...v, name: e.target.value }))} />
      <Input label="Preco" type="number" value={String(payload.price)} onChange={(e) => setPayload((v) => ({ ...v, price: Number(e.target.value) }))} />
      <Input label="Quantidade" type="number" value={String(payload.quantity)} onChange={(e) => setPayload((v) => ({ ...v, quantity: Number(e.target.value) }))} />
      <Input label="Inicio" type="datetime-local" value={payload.startDate} onChange={(e) => setPayload((v) => ({ ...v, startDate: e.target.value }))} />
      <Input label="Fim" type="datetime-local" value={payload.endDate} onChange={(e) => setPayload((v) => ({ ...v, endDate: e.target.value }))} />
      <Button type="submit">Salvar lote</Button>
    </form>
  );
}
