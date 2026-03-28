"use client";

import { Search } from "lucide-react";
import { useMemo, useState } from "react";
import { EventCard } from "@/components/events/EventCard";
import { EventForm } from "@/components/events/EventForm";
import { Button } from "@/components/ui/Button";
import { Modal } from "@/components/ui/Modal";
import { api } from "@/lib/api";
import { useEvents } from "@/lib/hooks/useEvents";

const tabs = ["Todos", "draft", "active", "completed", "cancelled"];

export default function EventsPage() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [activeTab, setActiveTab] = useState("Todos");
  const { events, loading, refresh } = useEvents();

  const filtered = useMemo(() => {
    return events.filter((event) => {
      const byTab = activeTab === "Todos" || event.status === activeTab;
      const byQuery = event.name.toLowerCase().includes(query.toLowerCase());
      return byTab && byQuery;
    });
  }, [activeTab, events, query]);

  return (
    <main style={{ display: "grid", gap: "1rem" }}>
      <section className="card" style={{ padding: "1rem", display: "grid", gap: "0.9rem" }}>
        <div style={{ display: "flex", justifyContent: "space-between", gap: "0.7rem", alignItems: "center", flexWrap: "wrap" }}>
          <h1 style={{ margin: 0, color: "var(--primary)" }}>Eventos</h1>
          <Button onClick={() => setOpen(true)}>+ Novo Evento</Button>
        </div>

        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
          {tabs.map((tab) => (
            <button key={tab} type="button" className={activeTab === tab ? "button-primary" : "button-ghost"} onClick={() => setActiveTab(tab)}>
              {tab === "draft" ? "Rascunho" : tab === "active" ? "Ativos" : tab === "completed" ? "Concluidos" : tab === "cancelled" ? "Cancelados" : "Todos"}
            </button>
          ))}
        </div>

        <label style={{ position: "relative", display: "block" }}>
          <Search size={16} style={{ position: "absolute", left: 10, top: 12, color: "var(--text-muted)" }} />
          <input className="input-field" style={{ paddingLeft: "2rem" }} placeholder="Buscar evento" value={query} onChange={(e) => setQuery(e.target.value)} />
        </label>
      </section>

      <section className="events-grid">
        {loading ? <p className="muted">Carregando...</p> : null}
        {!loading && filtered.length === 0 ? <p className="muted">Nenhum evento encontrado.</p> : null}
        {filtered.map((event) => (
          <EventCard key={event.id} event={event} />
        ))}
      </section>

      <Modal open={open} title="Novo Evento" onClose={() => setOpen(false)}>
        <EventForm
          onSubmit={async (payload) => {
            await api.createEvent(payload);
            setOpen(false);
            refresh();
          }}
          onCancel={() => setOpen(false)}
        />
      </Modal>
    </main>
  );
}
