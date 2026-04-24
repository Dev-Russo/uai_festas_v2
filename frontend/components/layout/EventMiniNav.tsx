"use client";

import Link from "next/link";
import { useAuth } from "@/lib/hooks/useAuth";

export function EventMiniNav({ eventId }: { eventId: string }) {
  const { userType, tokenPayload } = useAuth();
  const isCommissioner = userType === "commissioner";
  const isFullAccess = tokenPayload?.full_access ?? false;

  return (
    <nav>
      <Link href={`/events/${eventId}/dashboard`}>Dashboard</Link>
      <Link href={`/events/${eventId}/products`}>Lotes</Link>
      <Link href={`/events/${eventId}/sales`}>Vendas</Link>
      {(!isCommissioner || isFullAccess) && (
        <Link href={`/events/${eventId}/commissioners`}>Comissários</Link>
      )}
    </nav>
  );
}
