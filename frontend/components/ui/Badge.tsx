import { ReactNode } from "react";

type Status = string;

const statusConfig: Record<string, { label: string; bg: string; color: string }> = {
  draft: { label: "Rascunho", bg: "#F3F4F6", color: "#6B7280" },
  active: { label: "Ativo", bg: "#D1FAE5", color: "#059669" },
  completed: { label: "Concluido", bg: "#DBEAFE", color: "#2563EB" },
  cancelled: { label: "Cancelado", bg: "#FEE2E2", color: "#DC2626" },
  paid: { label: "Pago", bg: "#D1FAE5", color: "#059669" },
  checked_in: { label: "Check-in", bg: "#EDE9FE", color: "#7C3AED" },
};

export function Badge({ status, children }: { status: Status; children?: ReactNode }) {
  const cfg = statusConfig[status] ?? {
    label: status,
    bg: "var(--surface-2)",
    color: "var(--text-secondary)",
  };
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        borderRadius: 999,
        padding: "0.25rem 0.65rem",
        fontSize: "0.77rem",
        background: cfg.bg,
        color: cfg.color,
        fontWeight: 700,
      }}
    >
      {children ?? cfg.label}
    </span>
  );
}
