import {
  Commissioner,
  CreateCommissionerDTO,
  CreateEventDTO,
  CreateProductDTO,
  CreateProductGroupDTO,
  CreateSaleDTO,
  DashboardData,
  Event,
  Product,
  ProductGroup,
  ProductGroupMembership,
  Sale,
  UpdateProductGroupDTO,
  User,
  UserType,
} from "@/types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

function normalizeDashboard(data: Record<string, unknown>): DashboardData {
  const salesByProduct = Array.isArray(data.sales_by_product) ? data.sales_by_product : [];
  const salesByDay = Array.isArray(data.sales_by_day) ? data.sales_by_day : [];
  return {
    totalPaidSales: Number(data.total_paid_sales ?? 0),
    totalCancelledSales: Number(data.total_canceled_sales ?? 0),
    totalCheckins: Number(data.total_checkins ?? 0),
    totalRevenue: Number(data.total_revenue ?? 0),
    averageTicket: Number(data.average_ticket ?? 0),
    checkinRate: Number(data.checkin_rate ?? 0),
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

function normalizeSale(item: Record<string, unknown>): Sale {
  const code = item.unique_code ?? item.code;
  const checkin = item.checkin_at ?? item.checkinAt ?? null;
  return {
    id: String(item.id ?? ""),
    productId: String(item.product_id ?? item.productId ?? ""),
    buyerName: String(item.buyer_name ?? item.buyerName ?? ""),
    buyerEmail: String(item.buyer_email ?? item.buyerEmail ?? ""),
    paymentMethod: String(item.method_of_payment ?? item.paymentMethod ?? "pix"),
    price: Number(item.price ?? 0),
    status: String(item.status ?? "pending") as Sale["status"],
    code: code ? String(code) : undefined,
    createdAt: String(item.sale_date ?? item.createdAt ?? ""),
    checkinAt: checkin ? String(checkin) : null,
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

function normalizeCommissioner(item: Record<string, unknown>): Commissioner {
  return {
    id: String(item.id ?? ""),
    username: String(item.username ?? ""),
    name: String(item.name ?? ""),
    role: (item.role ?? "commissioner") as Commissioner["role"],
    fullAccess: Boolean(item.full_access ?? item.fullAccess ?? false),
    eventId: String(item.event_id ?? item.eventId ?? ""),
    commissionerGroupId: item.commissioner_group_id != null ? String(item.commissioner_group_id) : null,
    isActive: Boolean(item.is_active ?? item.isActive ?? true),
  };
}

function normalizeProduct(item: Record<string, unknown>): Product {
  return {
    id: String(item.id ?? ""),
    eventId: item.event_id != null ? String(item.event_id) : undefined,
    name: String(item.name ?? ""),
    price: Number(item.price ?? 0),
    quantity: item.available_quantity != null ? Number(item.available_quantity) : undefined,
    startDate: item.start_selling_date ? String(item.start_selling_date) : undefined,
    endDate: item.end_selling_date ? String(item.end_selling_date) : undefined,
  };
}

function normalizeProductGroupMembership(item: Record<string, unknown>): ProductGroupMembership {
  const product = (item.product ?? {}) as Record<string, unknown>;
  return {
    productId: String(item.product_id ?? item.productId ?? ""),
    groupId: String(item.group_id ?? item.groupId ?? ""),
    isActive: Boolean(item.is_active ?? item.isActive ?? true),
    product: {
      id: String(product.id ?? ""),
      name: String(product.name ?? ""),
      price: Number(product.price ?? 0),
      isActive: Boolean(product.is_active ?? product.isActive ?? true),
    },
  };
}

function normalizeProductGroup(item: Record<string, unknown>): ProductGroup {
  const childrenRaw = Array.isArray(item.children) ? item.children : [];
  const membershipsRaw = Array.isArray(item.memberships) ? item.memberships : [];
  return {
    id: String(item.id ?? ""),
    name: String(item.name ?? ""),
    eventId: String(item.event_id ?? item.eventId ?? ""),
    parentGroupId: item.parent_group_id != null ? String(item.parent_group_id) : null,
    isDefault: Boolean(item.is_default ?? item.isDefault ?? false),
    isActive: Boolean(item.is_active ?? item.isActive ?? true),
    children: childrenRaw.map((child) => normalizeProductGroup(child as Record<string, unknown>)),
    memberships: membershipsRaw.map((membership) => normalizeProductGroupMembership(membership as Record<string, unknown>)),
  };
}

export const api = {
  login: async (identifier: string, password: string): Promise<{ token: string; userType: UserType; eventId: number | null }> => {
    const body = new URLSearchParams();
    body.set("username", identifier);
    body.set("password", password);

    const res = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });

    if (!res.ok) {
      throw new Error("Credenciais invalidas");
    }

    const payload = (await res.json()) as { access_token: string; user_type: UserType; event_id: number | null };
    return { token: payload.access_token, userType: payload.user_type ?? "user", eventId: payload.event_id ?? null };
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

  getProducts: async (eventId: string) => {
    const data = await request<Record<string, unknown>[]>(`/events/${eventId}/products/`);
    return data.map(normalizeProduct);
  },
  createProduct: (eventId: string, data: CreateProductDTO) =>
    request(`/events/${eventId}/products/`, {
      method: "POST",
      body: JSON.stringify({
        name: data.name,
        price: data.price,
        available_quantity: data.quantity,
        start_selling_date: data.startDate,
        end_selling_date: data.endDate,
      }),
    }),
  updateProduct: (eventId: string, productId: string, data: CreateProductDTO) =>
    request(`/events/${eventId}/products/${productId}`, {
      method: "PUT",
      body: JSON.stringify({
        name: data.name,
        price: data.price,
        available_quantity: data.quantity,
        start_selling_date: data.startDate || null,
        end_selling_date: data.endDate || null,
      }),
    }),
  deleteProduct: (eventId: string, productId: string) => request(`/events/${eventId}/products/${productId}`, { method: "DELETE" }),

  getProductGroups: async (eventId: string) => {
    const data = await request<Record<string, unknown>[]>(`/events/${eventId}/product-groups/`);
    return data.map((item) => normalizeProductGroup(item));
  },
  createProductGroup: async (eventId: string, data: CreateProductGroupDTO) => {
    const result = await request<Record<string, unknown>>(`/events/${eventId}/product-groups/`, {
      method: "POST",
      body: JSON.stringify({
        name: data.name,
        parent_group_id: data.parentGroupId != null && data.parentGroupId !== "" ? Number(data.parentGroupId) : null,
        is_default: data.isDefault ?? false,
      }),
    });
    return normalizeProductGroup(result);
  },
  updateProductGroup: async (eventId: string, groupId: string, data: UpdateProductGroupDTO) => {
    const body: Record<string, unknown> = {};
    if (data.name !== undefined) body.name = data.name;
    if (data.isDefault !== undefined) body.is_default = data.isDefault;
    if (data.isActive !== undefined) body.is_active = data.isActive;
    const result = await request<Record<string, unknown>>(`/events/${eventId}/product-groups/${groupId}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    });
    return normalizeProductGroup(result);
  },
  deleteProductGroup: (eventId: string, groupId: string) =>
    request(`/events/${eventId}/product-groups/${groupId}`, { method: "DELETE" }),
  addProductToGroup: async (eventId: string, groupId: string, productId: string) => {
    const result = await request<Record<string, unknown>>(
      `/events/${eventId}/product-groups/${groupId}/products?product_id=${encodeURIComponent(productId)}`,
      { method: "POST" },
    );
    return normalizeProductGroupMembership(result);
  },
  toggleProductInGroup: async (eventId: string, groupId: string, productId: string, isActive: boolean) => {
    const result = await request<Record<string, unknown>>(`/events/${eventId}/product-groups/${groupId}/products/${productId}`, {
      method: "PATCH",
      body: JSON.stringify({ is_active: isActive }),
    });
    return normalizeProductGroupMembership(result);
  },
  removeProductFromGroup: (eventId: string, groupId: string, productId: string) =>
    request(`/events/${eventId}/product-groups/${groupId}/products/${productId}`, { method: "DELETE" }),

  getSales: async (eventId: string) => {
    const data = await request<Record<string, unknown>[]>(`/events/${eventId}/sales/`);
    return data.map((item) => normalizeSale(item));
  },
  getSale: async (eventId: string, saleId: string) => {
    const data = await request<Record<string, unknown>>(`/events/${eventId}/sales/${saleId}`);
    return normalizeSale(data);
  },
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

  getCommissioners: async (eventId: string) => {
    const data = await request<Record<string, unknown>[]>(`/events/${eventId}/commissioners/`);
    return data.map(normalizeCommissioner);
  },
  createCommissioner: (eventId: string, data: CreateCommissionerDTO) =>
    request<Record<string, unknown>>(`/events/${eventId}/commissioners/`, {
      method: "POST",
      body: JSON.stringify({
        username: data.username,
        name: data.name,
        password: data.password,
        role: data.role,
        full_access: data.fullAccess,
        is_active: true,
      }),
    }).then(normalizeCommissioner),
  updateCommissioner: async (eventId: string, commissionerId: string, data: Partial<CreateCommissionerDTO> & { isActive?: boolean; commissionerGroupId?: number | null }) => {
    const body: Record<string, unknown> = {};
    if (data.name !== undefined) body.name = data.name;
    if (data.role !== undefined) body.role = data.role;
    if (data.fullAccess !== undefined) body.full_access = data.fullAccess;
    if (data.isActive !== undefined) body.is_active = data.isActive;
    if (data.password !== undefined) body.password = data.password;
    if (data.commissionerGroupId !== undefined) body.commissioner_group_id = data.commissionerGroupId;
    const result = await request<Record<string, unknown>>(`/events/${eventId}/commissioners/${commissionerId}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    });
    return normalizeCommissioner(result);
  },
  deleteCommissioner: (eventId: string, commissionerId: string) =>
    request(`/events/${eventId}/commissioners/${commissionerId}`, { method: "DELETE" }),
  getCommissionerMe: async () => {
    const data = await request<Record<string, unknown>>("/commissioners/me");
    return normalizeCommissioner(data);
  },
};
