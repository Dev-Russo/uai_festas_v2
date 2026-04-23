import Link from "next/link";
import type { ReactNode } from "react";

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
        <nav>
          <Link href={`/events/${id}/dashboard`}>Dashboard</Link>
          <Link href={`/events/${id}/products`}>Lotes</Link>
          <Link href={`/events/${id}/sales`}>Vendas</Link>
          <Link href={`/events/${id}/commissioners`}>Comissários</Link>
        </nav>
      </aside>
      <div>{children}</div>
    </section>
  );
}
