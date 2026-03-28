import { InputHTMLAttributes, ReactNode } from "react";

type Props = InputHTMLAttributes<HTMLInputElement> & {
  label: string;
  error?: string;
  rightSlot?: ReactNode;
};

export function Input({ label, error, rightSlot, ...props }: Props) {
  return (
    <label style={{ display: "grid", gap: "0.35rem" }}>
      <span style={{ fontSize: "0.9rem", color: "var(--text-secondary)" }}>{label}</span>
      <div style={{ position: "relative" }}>
        <input className="input-field" {...props} style={{ paddingRight: rightSlot ? "2.5rem" : undefined }} />
        {rightSlot ? <span style={{ position: "absolute", right: 10, top: 11 }}>{rightSlot}</span> : null}
      </div>
      {error ? <small style={{ color: "var(--danger)" }}>{error}</small> : null}
    </label>
  );
}
