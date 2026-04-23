import { Badge } from "@/components/ui/Badge";

export function EventStatusBadge({ status }: { status: string }) {
  return <Badge status={status} />;
}
