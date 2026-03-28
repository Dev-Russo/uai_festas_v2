import { Badge } from "@/components/ui/Badge";
import { Sale } from "@/types";

export function SaleRow({ sale }: { sale: Sale }) {
  return (
    <tr>
      <td>{sale.code || sale.id}</td>
      <td>{sale.buyerName}</td>
      <td>{sale.productId}</td>
      <td>{new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(sale.price)}</td>
      <td>{sale.paymentMethod}</td>
      <td><Badge status={sale.status} /></td>
      <td>{sale.createdAt ? new Date(sale.createdAt).toLocaleDateString("pt-BR") : "-"}</td>
    </tr>
  );
}
