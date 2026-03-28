"use client";

type SideMenuProps = {
  active: "dashboard" | "products" | "sales";
  onSelect: (next: "dashboard" | "products" | "sales") => void;
  eventName: string;
  onLogout: () => void;
};

const menuItems: Array<{ key: "dashboard" | "products" | "sales"; label: string }> = [
  { key: "dashboard", label: "Dashboard" },
  { key: "products", label: "Produtos" },
  { key: "sales", label: "Vendas" },
];

export function SideMenu({ active, onSelect, eventName, onLogout }: SideMenuProps) {
  return (
    <aside
      className="card"
      style={{
        padding: "1rem",
        display: "flex",
        flexDirection: "column",
        gap: "0.9rem",
      }}
    >
      <div>
        <p className="muted" style={{ fontSize: "0.78rem", marginBottom: "0.35rem" }}>
          Evento selecionado
        </p>
        <h2 style={{ margin: 0, fontSize: "1.1rem", lineHeight: 1.2 }}>{eventName}</h2>
      </div>

      <nav style={{ display: "grid", gap: "0.55rem" }}>
        {menuItems.map((item) => {
          const isActive = item.key === active;
          return (
            <button
              key={item.key}
              type="button"
              onClick={() => onSelect(item.key)}
              className={isActive ? "button-primary" : "button-ghost"}
              style={{ textAlign: "left" }}
            >
              {item.label}
            </button>
          );
        })}
      </nav>

      <div style={{ marginTop: "auto" }}>
        <button type="button" className="button-ghost" onClick={onLogout} style={{ width: "100%" }}>
          Sair
        </button>
      </div>
    </aside>
  );
}
