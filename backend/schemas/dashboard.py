from pydantic import BaseModel

class DashboardResponse(BaseModel):
    total_paid_sales: int
    total_canceled_sales: int
    total_revenue: float
    average_ticket: float
    sales_by_product: list[dict]  # Exemplo: [{"product_name": "Ingresso VIP", "sales_count": 100}]
    sales_by_day: list[dict]      # Exemplo: [{"date": "2024-01-01", "sales_count": 20}]
    cancellation_rate: float