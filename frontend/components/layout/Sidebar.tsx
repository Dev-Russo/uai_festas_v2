"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { CalendarDays, LayoutDashboard, LogOut, Ticket, UserRound } from "lucide-react";
import { Avatar } from "@/components/ui/Avatar";
import { clearToken } from "@/lib/auth";

const items = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/events", label: "Eventos", icon: CalendarDays },
  { href: "/profile", label: "Perfil", icon: UserRound },
];

export function Sidebar({ userName, role }: { userName?: string; role?: string }) {
  const pathname = usePathname();
  const router = useRouter();

  return (
    <aside className="sidebar-shell">
      <div>
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

      <nav className="sidebar-nav">
        {items.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
          return (
            <Link href={item.href} key={item.href} className={isActive ? "active" : ""}>
              <Icon size={18} />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <button
        className="logout-btn"
        onClick={() => {
          clearToken();
          router.push("/login");
        }}
        type="button"
      >
        <LogOut size={16} /> Sair
      </button>
    </aside>
  );
}
