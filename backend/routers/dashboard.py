from backend.schemas.dashboard import DashboardResponse
from backend.dependencies import get_db
from backend.utils.security import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.models.event import Event
from backend.models.sales import Sales
from backend.models.products import Product
from backend.enums.sales import SaleStatus
from sqlalchemy import func

router = APIRouter(prefix="/events/{event_id}/dashboard", tags=["Dashboard"])

@router.get("/", response_model=DashboardResponse)
def get_event_dashboard(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verificar se o evento existe e pertence ao usuário
    event = db.query(Event).filter(Event.id == event_id, Event.user_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found or access denied")
    
    # Calcular as métricas do dashboard

    # Total de vendas pagas
    total_paid_sales = db.query(Event).join(Product).join(Sales).filter(
        Event.id == event_id, 
        Sales.status == "paid"
    ).count()
    
    # Total de vendas canceladas
    total_canceled_sales = db.query(Event).join(Product).join(Sales).filter(
        Event.id == event_id, 
        Sales.status == SaleStatus.cancelled
    ).count()
    
    # Total de receita
    total_revenue = db.query(Event).join(Product).join(Sales).filter(
        Event.id == event_id, 
        Sales.status == SaleStatus.paid
    ).with_entities(func.sum(Product.price)).scalar() or 0.0
    
    # Ticket médio
    average_ticket = total_revenue / total_paid_sales if total_paid_sales > 0 else 0

    # Vendas por produto
    sales_by_product_raw = db.query(
        Product.name, 
        func.count(Sales.id)
    ).join(Sales).filter(
        Product.event_id == event_id, 
        Sales.status == "paid"
    ).group_by(Product.name).all()
    
    # Vendas por dia (últimos 30 dias)
    sales_by_day_raw = db.query(
        func.date(Sales.sale_date), 
        func.count(Sales.id)
    ).join(Product).join(Event).filter(
        Event.id == event_id, 
        Sales.status == SaleStatus.paid
    ).group_by(
        func.date(Sales.sale_date)
    ).order_by(
        func.date(Sales.sale_date).desc()
    ).limit(30).all()
    
    # Taxa de Check-in
    total_checkin = db.query(Event).join(Product).join(Sales).filter(
        Event.id == event_id, 
        Sales.status == SaleStatus.check_in
    ).count()

    # Taxa de cancelamento
    cancellation_rate = (total_canceled_sales / (total_paid_sales + total_canceled_sales + total_checkin)) if (total_paid_sales + total_canceled_sales) > 0 else 0.0

    ## Formatar os resultados para o modelo de resposta
    sales_by_product = [{"product_name": name, "sales_count": count} for name, count in sales_by_product_raw]
    sales_by_day = [{"sale_date": date, "sales_count": count} for date, count in sales_by_day_raw]

    return DashboardResponse(
        total_paid_sales=total_paid_sales,
        total_canceled_sales=total_canceled_sales,
        total_revenue=total_revenue,
        average_ticket=average_ticket,
        sales_by_product=sales_by_product,     
        sales_by_day=sales_by_day,
        cancellation_rate=cancellation_rate
    )