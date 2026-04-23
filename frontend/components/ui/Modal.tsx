"use client";

import { PropsWithChildren } from "react";
import { X } from "lucide-react";

export function Modal({
  open,
  title,
  onClose,
  children,
}: PropsWithChildren<{ open: boolean; title: string; onClose: () => void }>) {
  if (!open) {
    return null;
  }
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(26,26,46,0.35)",
        backdropFilter: "blur(4px)",
        display: "grid",
        placeItems: "center",
        zIndex: 40,
        padding: "1rem",
      }}
    >
      <div className="card" style={{ width: "min(560px, 100%)", padding: "1rem" }}>
        <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <h3 style={{ margin: 0 }}>{title}</h3>
          <button className="button-ghost" onClick={onClose} type="button" aria-label="Fechar">
            <X size={16} />
          </button>
        </header>
        <div style={{ marginTop: "0.8rem" }}>{children}</div>
      </div>
    </div>
  );
}
