"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { CalendarDays, LayoutDashboard, LogOut, Ticket, UserRound } from "lucide-react";
import { Avatar } from "@/components/ui/Avatar";
import { clearToken } from "@/lib/auth";
import { UserType } from "@/types";

const adminItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/events", label: "Eventos", icon: CalendarDays },
  { href: "/profile", label: "Perfil", icon: UserRound },
];

export function Sidebar({
  userName,
  role,
  userType,
  eventId,
}: {
  userName?: string;
  role?: string;
  userType?: UserType;
  eventId?: number | null;
}) {
  const pathname = usePathname();
  const router = useRouter();

  const isCommissioner = userType === "commissioner";
  const items =
    isCommissioner && eventId
      ? [{ href: `/events/${eventId}/dashboard`, label: "Meu Evento", icon: LayoutDashboard }]
      : adminItems;

  return (
    <aside className="sidebar-shell">
      <div className="sidebar-top">
        <div className="sidebar-logo">
          <Ticket size={18} /> <span>Uai Festas</span>
        </div>
        <div className="sidebar-user">
          <Avatar name={userName} />
          <div>
            <p>{userName || "Usuario"}</p>
            <small>{role || "Produtor"}</small>
          </div>
        </div>
      </div>

      <div className="sidebar-nav-wrapper">
        <nav className="sidebar-nav">
          {items.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
            return (
              <Link href={item.href} key={item.href} className={isActive ? "active" : ""}>
                <Icon size={20} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      <div style={{ marginTop: "auto" }}>
        <button
          className="logout-btn"
          onClick={() => {
            clearToken();
            router.push("/login");
          }}
          type="button"
        >
          <LogOut size={20} /> Sair
        </button>
      </div>
    </aside>
  );
}
