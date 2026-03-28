"use client";

import { FormEvent, useState } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { CreateEventDTO } from "@/types";

export function EventForm({
  onSubmit,
  onCancel,
}: {
  onSubmit: (payload: CreateEventDTO) => Promise<void>;
  onCancel: () => void;
}) {
  const [payload, setPayload] = useState<CreateEventDTO>({ name: "", description: "", date: "", location: "" });
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    await onSubmit(payload);
    setLoading(false);
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: "grid", gap: "0.75rem" }}>
      <Input label="Nome" value={payload.name} onChange={(e) => setPayload((prev) => ({ ...prev, name: e.target.value }))} required />
      <label style={{ display: "grid", gap: "0.35rem" }}>
        <span style={{ fontSize: "0.9rem", color: "var(--text-secondary)" }}>Descricao</span>
        <textarea
          className="input-field"
          value={payload.description}
          onChange={(e) => setPayload((prev) => ({ ...prev, description: e.target.value }))}
          rows={3}
        />
      </label>
      <Input
        label="Data e hora"
        type="datetime-local"
        value={payload.date}
        onChange={(e) => setPayload((prev) => ({ ...prev, date: e.target.value }))}
        required
      />
      <Input label="Local" value={payload.location} onChange={(e) => setPayload((prev) => ({ ...prev, location: e.target.value }))} required />
      <div style={{ display: "flex", gap: "0.5rem", justifyContent: "flex-end" }}>
        <Button type="button" variant="ghost" onClick={onCancel}>Cancelar</Button>
        <Button type="submit" disabled={loading}>{loading ? "Criando..." : "Criar evento"}</Button>
      </div>
    </form>
  );
}
