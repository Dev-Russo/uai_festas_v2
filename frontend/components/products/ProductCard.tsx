import { Product } from "@/types";

export function ProductCard({ product }: { product: Product }) {
  return (
    <article className="card" style={{ padding: "0.9rem" }}>
      <h4 style={{ marginTop: 0 }}>{product.name}</h4>
      <p className="muted">Preco: {new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(product.price)}</p>
      <div style={{ height: 8, borderRadius: 999, background: "#EEE8FF", overflow: "hidden" }}>
        <div style={{ width: "40%", height: "100%", background: "var(--primary)" }} />
      </div>
    </article>
  );
}
