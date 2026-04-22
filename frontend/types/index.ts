export type Role = "admin" | "producer";
export type CommissionerRole = "commissioner" | "commissioner_admin";
export type EventStatus = "draft" | "active" | "completed" | "cancelled" | "Not Realized";
export type SaleStatus = "paid" | "cancelled" | "refunded" | "pending";
export type PaymentMethod = "credit_card" | "debit_card" | "pix" | "cash";
export type UserType = "user" | "commissioner";

export interface User {
  id: string;
  name: string;
  email: string;
  role: Role;
  createdAt?: string;
}

export interface Event {
  id: string;
  name: string;
  description: string;
  date?: string;
  location?: string;
  status: EventStatus | string;
  event_date?: string;
  createdAt?: string;
}

export interface Product {
  id: string;
  eventId?: string;
  event_id?: string;
  name: string;
  price: number;
  quantity?: number;
  startDate?: string;
  endDate?: string;
}

export interface Sale {
  id: string;
  eventId?: string;
  productId: string;
  buyerName: string;
  buyerEmail: string;
  paymentMethod: PaymentMethod | string;
  price: number;
  status: SaleStatus;
  code?: string;
  createdAt?: string;
  checkinAt?: string | null;
}

export interface DashboardData {
  totalPaidSales: number;
  totalCancelledSales: number;
  totalRevenue: number;
  averageTicket: number;
  salesByProduct: { productName: string; count: number; revenue?: number }[];
  salesByDay: { date: string; count: number; revenue?: number }[];
  cancellationRate: number;
}

export interface CreateEventDTO {
  name: string;
  description: string;
  date: string;
  location: string;
}

export interface CreateProductDTO {
  name: string;
  price: number;
  quantity: number;
  startDate: string;
  endDate: string;
}

export interface Commissioner {
  id: string;
  username: string;
  name: string;
  role: CommissionerRole;
  fullAccess: boolean;
  eventId: string;
  commissionerGroupId?: string | null;
  isActive: boolean;
}

export interface TokenPayload {
  sub: string;
  role: string;
  user_type: UserType;
  event_id?: number;
  commissioner_group_id?: number;
  full_access?: boolean;
  exp: number;
}

export interface CreateCommissionerDTO {
  username: string;
  name: string;
  password: string;
  role: CommissionerRole;
  fullAccess: boolean;
}

export interface CreateSaleDTO {
  productId: string;
  buyerName: string;
  buyerEmail: string;
  paymentMethod: PaymentMethod;
}
