from pydantic import BaseModel

class DashboardResponse(BaseModel):
    total_paid_sales: int
    total_canceled_sales: int
    total_checkins: int
    total_revenue: float
    average_ticket: float
    checkin_rate: float
    sales_by_product: list[dict]
    sales_by_day: list[dict]
    cancellation_rate: float