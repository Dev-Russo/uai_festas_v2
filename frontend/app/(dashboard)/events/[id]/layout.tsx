import type { ReactNode } from "react";
import { EventMiniNav } from "@/components/layout/EventMiniNav";

export default async function EventSectionLayout({
  children,
  params,
}: {
  children: ReactNode;
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  return (
    <section className="event-section-layout">
      <aside className="event-mini-nav card">
        <h3>Evento #{id}</h3>
        <p className="muted">Navegacao rapida</p>
        <EventMiniNav eventId={id} />
      </aside>
      <div>{children}</div>
    </section>
  );
}
