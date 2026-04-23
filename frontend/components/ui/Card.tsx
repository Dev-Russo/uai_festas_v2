import { PropsWithChildren } from "react";

export function Card({ children }: PropsWithChildren) {
  return <article className="card" style={{ padding: "1rem" }}>{children}</article>;
}
