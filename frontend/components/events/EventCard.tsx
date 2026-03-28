import Link from "next/link";
import { CalendarDays, MapPin } from "lucide-react";
import { Event } from "@/types";
import { EventStatusBadge } from "@/components/events/EventStatusBadge";

export function EventCard({ event }: { event: Event }) {
  return (
    <article className="card event-card">
      <EventStatusBadge status={event.status} />
      <h3>{event.name}</h3>
      <p><MapPin size={14} /> {event.location || "Local nao informado"}</p>
      <p><CalendarDays size={14} /> {event.event_date ? new Date(event.event_date).toLocaleDateString("pt-BR") : "Data nao informada"}</p>
      <Link href={`/events/${event.id}/dashboard`} className="event-link">Abrir dashboard</Link>
    </article>
  );
}
