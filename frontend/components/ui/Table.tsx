import { PropsWithChildren } from "react";

export function Table({ children }: PropsWithChildren) {
  return (
    <div style={{ overflowX: "auto", border: "1px solid var(--border)", borderRadius: 12 }}>
      <table style={{ width: "100%", borderCollapse: "collapse", minWidth: 760 }}>{children}</table>
    </div>
  );
}
