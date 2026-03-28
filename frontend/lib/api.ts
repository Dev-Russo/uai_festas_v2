import {
  CreateEventDTO,
  CreateProductDTO,
  CreateSaleDTO,
  DashboardData,
  Event,
  Product,
  Sale,
  User,
} from "@/types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

function normalizeDashboard(data: Record<string, unknown>): DashboardData {
  const salesByProduct = Array.isArray(data.sales_by_product) ? data.sales_by_product : [];
  const salesByDay = Array.isArray(data.sales_by_day) ? data.sales_by_day : [];
  return {
    totalPaidSales: Number(data.total_paid_sales ?? 0),
    totalCancelledSales: Number(data.total_canceled_sales ?? 0),
    totalRevenue: Number(data.total_revenue ?? 0),
    averageTicket: Number(data.average_ticket ?? 0),
    salesByProduct: salesByProduct.map((item) => {
      const typed = item as Record<string, unknown>;
      return {
        productName: String(typed.product_name ?? "Sem nome"),
        count: Number(typed.sales_count ?? 0),
      };
    }),
    salesByDay: salesByDay.map((item) => {
      const typed = item as Record<string, unknown>;
      return {
        date: String(typed.sale_date ?? ""),
        count: Number(typed.sales_count ?? 0),
      };
    }),
    cancellationRate: Number(data.cancellation_rate ?? 0),
  };
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const isBrowser = typeof window !== "undefined";
  const token = isBrowser ? window.localStorage.getItem("token") : null;
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options?.headers,
    },
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(await res.text());
  }
  if (res.status === 204) {
    return {} as T;
  }
  return (await res.json()) as T;
}

export const api = {
  login: async (email: string, password: string) => {
    const body = new URLSearchParams();
    body.set("username", email);
    body.set("password", password);

    const res = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body,
    });

    if (!res.ok) {
      throw new Error("Credenciais invalidas");
    }

    const payload = (await res.json()) as { access_token: string };
    return { token: payload.access_token };
  },

  register: (name: string, email: string, password: string) =>
    request("/auth/register", {
      method: "POST",
      body: JSON.stringify({ name, email, password, role: "producer", is_active: true }),
    }),

  getMe: () => request<User>("/users/me"),
  updateMe: (data: Partial<User>) => request("/users/me", { method: "PUT", body: JSON.stringify(data) }),

  getEvents: () => request<Event[]>("/events/"),
  getEvent: (id: string) => request<Event>(`/events/${id}`),
  createEvent: (data: CreateEventDTO) =>
    request("/events/", {
      method: "POST",
      body: JSON.stringify({
        name: data.name,
        description: data.description,
        status: "draft",
        event_date: data.date,
        sales_start_date: data.date,
      }),
    }),
  updateEvent: (id: string, data: Partial<Event>) => request(`/events/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteEvent: (id: string) => request(`/events/${id}`, { method: "DELETE" }),

  getProducts: (eventId: string) => request<Product[]>(`/events/${eventId}/products/`),
  createProduct: (eventId: string, data: CreateProductDTO) =>
    request(`/events/${eventId}/products/`, {
      method: "POST",
      body: JSON.stringify({
        name: data.name,
        price: data.price,
        start_selling_date: data.startDate,
        end_selling_date: data.endDate,
      }),
    }),
  updateProduct: (eventId: string, productId: string, data: Partial<Product>) =>
    request(`/events/${eventId}/products/${productId}`, { method: "PUT", body: JSON.stringify(data) }),
  deleteProduct: (eventId: string, productId: string) => request(`/events/${eventId}/products/${productId}`, { method: "DELETE" }),

  getSales: (eventId: string) => request<Sale[]>(`/events/${eventId}/sales/`),
  getSale: (eventId: string, saleId: string) => request<Sale>(`/events/${eventId}/sales/${saleId}`),
  createSale: (eventId: string, data: CreateSaleDTO) =>
    request(`/events/${eventId}/sales/`, {
      method: "POST",
      body: JSON.stringify({
        product_id: Number(data.productId),
        buyer_name: data.buyerName,
        buyer_email: data.buyerEmail,
        method_of_payment: data.paymentMethod,
        sale_date: new Date().toISOString(),
        status: "paid",
      }),
    }),
  cancelSale: (eventId: string, saleId: string) => request(`/events/${eventId}/sales/${saleId}/cancel`, { method: "PATCH" }),
  checkinSale: (eventId: string, saleId: string) => request(`/events/${eventId}/sales/${saleId}/check-in`, { method: "PATCH" }),

  getEventDashboard: async (eventId: string) => {
    const data = await request<Record<string, unknown>>(`/events/${eventId}/dashboard/`);
    return normalizeDashboard(data);
  },
};
