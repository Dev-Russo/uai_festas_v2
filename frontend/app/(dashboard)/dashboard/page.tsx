"use client";

import Link from "next/link";
import { EventCard } from "@/components/events/EventCard";
import { useAuth } from "@/lib/hooks/useAuth";
import { useEvents } from "@/lib/hooks/useEvents";

export default function DashboardPage() {
  const { user } = useAuth();
  const { events, loading } = useEvents();
  const recentEvents = events.slice(0, 6);

  return (
    <main style={{ display: "grid", gap: "1rem" }}>
      <section className="card" style={{ padding: "1rem" }}>
        <h1 style={{ marginTop: 0 }}>Ola, {user?.name || "Produtor"}! 👋</h1>
        <p className="muted">{new Date().toLocaleDateString("pt-BR", { dateStyle: "full" })}</p>
      </section>

      <section className="card" style={{ padding: "1rem" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <h2 style={{ marginTop: 0 }}>Meus Eventos Recentes</h2>
          <Link href="/events" className="button-ghost">Ver todos os eventos</Link>
        </div>
        {loading ? <p className="muted">Carregando eventos...</p> : null}
        {!loading && recentEvents.length === 0 ? <p className="muted">Nenhum evento encontrado.</p> : null}
        <div className="events-grid">
          {recentEvents.map((event) => (
            <EventCard key={event.id} event={event} />
          ))}
        </div>
      </section>
    </main>
  );
}
