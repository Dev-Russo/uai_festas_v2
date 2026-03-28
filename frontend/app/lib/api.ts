const baseURL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

function buildURL(path: string): string {
  return `${baseURL}${path}`;
}

export type EventItem = {
  id: number;
  user_id: number;
  name: string;
  description: string | null;
  status: string;
  event_date: string;
  sales_start_date: string;
};

export type DashboardResponse = {
  total_paid_sales: number;
  total_canceled_sales: number;
  total_revenue: number;
  average_ticket: number;
  sales_by_product: Array<{ product_name: string; sales_count: number }>;
  sales_by_day: Array<{ sale_date: string; sales_count: number }>;
  cancellation_rate: number;
};

export async function login(email: string, password: string): Promise<string> {
  const body = new URLSearchParams();
  body.set("username", email);
  body.set("password", password);

  const response = await fetch(buildURL("/auth/login"), {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });

  if (!response.ok) {
    throw new Error("Email ou senha invalidos.");
  }

  const data = (await response.json()) as { access_token: string };
  return data.access_token;
}

export async function getEvents(token: string): Promise<EventItem[]> {
  const response = await fetch(buildURL("/events/"), {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Nao foi possivel carregar seus eventos.");
  }

  return (await response.json()) as EventItem[];
}

export async function getEventById(eventId: string, token: string): Promise<EventItem> {
  const response = await fetch(buildURL(`/events/${eventId}`), {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Nao foi possivel carregar este evento.");
  }

  return (await response.json()) as EventItem;
}

export async function getDashboard(eventId: string, token: string): Promise<DashboardResponse> {
  const response = await fetch(buildURL(`/events/${eventId}/dashboard/`), {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Nao foi possivel carregar o dashboard.");
  }

  return (await response.json()) as DashboardResponse;
}
