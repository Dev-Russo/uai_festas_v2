"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { clearToken, getToken } from "../lib/auth";
import { EventItem, getEvents } from "../lib/api";

export default function EventsPage() {
  const router = useRouter();
  const [events, setEvents] = useState<EventItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.replace("/");
      return;
    }
    const authToken = token;

    async function loadEvents() {
      try {
        const result = await getEvents(authToken);
        setEvents(result);
      } catch (err) {
        const message = err instanceof Error ? err.message : "Nao foi possivel carregar os eventos.";
        setError(message);
      } finally {
        setLoading(false);
      }
    }

    loadEvents();
  }, [router]);

  function handleLogout() {
    clearToken();
    router.push("/");
  }

  return (
    <main className="page-shell" style={{ display: "grid", gap: "1rem" }}>
      <header
        className="card"
        style={{
          padding: "1rem 1.1rem",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: "0.8rem",
        }}
      >
        <div>
          <p style={{ margin: 0, fontFamily: "var(--font-plex-mono)", color: "var(--app-accent-strong)", fontSize: "0.82rem" }}>
            AREA DO PRODUTOR
          </p>
          <h1 style={{ margin: "0.25rem 0 0", fontSize: "1.6rem" }}>Meus Eventos</h1>
        </div>
        <button className="button-ghost" onClick={handleLogout} type="button">
          Sair
        </button>
      </header>

      <section className="card" style={{ padding: "1rem" }}>
        {loading ? <p className="muted">Carregando seus eventos...</p> : null}

        {!loading && error ? <p style={{ color: "var(--app-danger)" }}>{error}</p> : null}

        {!loading && !error && events.length === 0 ? (
          <p className="muted">Voce ainda nao possui eventos cadastrados.</p>
        ) : null}

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))",
            gap: "0.8rem",
          }}
        >
          {events.map((event) => (
            <button
              key={event.id}
              type="button"
              className="button-ghost"
              style={{
                textAlign: "left",
                padding: "0.85rem",
                background: "var(--app-surface)",
                display: "grid",
                gap: "0.45rem",
              }}
              onClick={() => router.push(`/events/${event.id}/dashboard`)}
            >
              <strong style={{ fontSize: "1rem" }}>{event.name}</strong>
              <span className="muted" style={{ fontSize: "0.86rem" }}>
                Status: {event.status}
              </span>
              <span className="muted" style={{ fontSize: "0.86rem" }}>
                Data: {new Date(event.event_date).toLocaleDateString("pt-BR")}
              </span>
            </button>
          ))}
        </div>
      </section>
    </main>
  );
}
