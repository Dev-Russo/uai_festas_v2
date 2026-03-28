"use client";

import { Bell } from "lucide-react";
import { usePathname } from "next/navigation";
import { Avatar } from "@/components/ui/Avatar";

function toTitle(pathname: string): string {
  const cleaned = pathname.replace(/^\//, "");
  if (!cleaned) return "Dashboard";
  return cleaned.split("/").map((part) => (part ? part[0].toUpperCase() + part.slice(1) : part)).join(" / ");
}

export function Topbar({ userName }: { userName?: string }) {
  const pathname = usePathname();
  return (
    <header className="topbar-shell">
      <p>{toTitle(pathname)}</p>
      <div>
        <button className="button-ghost" type="button" aria-label="Notificacoes">
          <Bell size={16} />
        </button>
        <Avatar name={userName} />
      </div>
    </header>
  );
}
