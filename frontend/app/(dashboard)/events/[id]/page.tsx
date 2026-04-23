"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Event } from "@/types";

export default function EventDetailsPage() {
  const { id } = useParams<{ id: string }>();
  const [event, setEvent] = useState<Event | null>(null);

  useEffect(() => {
    api.getEvent(String(id)).then(setEvent).catch(() => setEvent(null));
  }, [id]);

  if (!event) {
    return <main className="card" style={{ padding: "1rem" }}><p className="muted">Carregando evento...</p></main>;
  }

  return (
    <main style={{ display: "grid", gap: "1rem" }}>
      <section className="card" style={{ padding: "1rem" }}>
        <h1 style={{ marginTop: 0 }}>{event.name}</h1>
        <p className="muted">{event.description || "Sem descricao"}</p>
      </section>
      <section className="card" style={{ padding: "1rem", display: "flex", gap: "0.7rem", flexWrap: "wrap" }}>
        <Link className="button-ghost" href={`/events/${event.id}/dashboard`}>Dashboard</Link>
        <Link className="button-ghost" href={`/events/${event.id}/products`}>Lotes</Link>
        <Link className="button-ghost" href={`/events/${event.id}/sales`}>Vendas</Link>
      </section>
    </main>
  );
}
