from schemas.dashboard import DashboardResponse
from dependencies import get_db
from utils.security import get_current_actor
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.event import Event
from models.sales import Sales
from models.products import Product
from enums.sales import SaleStatus
from sqlalchemy import func

router = APIRouter(prefix="/events/{event_id}/dashboard", tags=["Dashboard"])

@router.get("/", response_model=DashboardResponse)
def get_event_dashboard(
    event_id: int,
    db: Session = Depends(get_db),
    actor=Depends(get_current_actor),
):
    from models.commissioner import Commissioner
    if isinstance(actor, Commissioner):
        if actor.event_id != event_id:
            raise HTTPException(status_code=403, detail="Acesso negado")
        event = db.query(Event).filter(Event.id == event_id).first()
    else:
        event = db.query(Event).filter(Event.id == event_id, Event.user_id == actor.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found or access denied")

    restrict_to_commissioner = isinstance(actor, Commissioner) and not actor.full_access

    total_paid_sales = db.query(Event).join(Product).join(Sales).filter(
        Event.id == event_id,
        Sales.status == "paid",
        *([Sales.commissioner_id == actor.id] if restrict_to_commissioner else []),
    ).count()

    total_canceled_sales = db.query(Event).join(Product).join(Sales).filter(
        Event.id == event_id,
        Sales.status == SaleStatus.cancelled,
        *([Sales.commissioner_id == actor.id] if restrict_to_commissioner else []),
    ).count()

    total_revenue = db.query(Event).join(Product).join(Sales).filter(
        Event.id == event_id,
        Sales.status == SaleStatus.paid,
        *([Sales.commissioner_id == actor.id] if restrict_to_commissioner else []),
    ).with_entities(func.sum(Product.price)).scalar() or 0.0

    average_ticket = total_revenue / total_paid_sales if total_paid_sales > 0 else 0

    total_checkins = db.query(Event).join(Product).join(Sales).filter(
        Event.id == event_id,
        Sales.checkin_at.isnot(None),
        *([Sales.commissioner_id == actor.id] if restrict_to_commissioner else []),
    ).count()

    checkin_rate = total_checkins / total_paid_sales if total_paid_sales > 0 else 0.0

    sales_by_product_raw = db.query(
        Product.name,
        func.count(Sales.id)
    ).join(Sales).filter(
        Product.event_id == event_id,
        Sales.status == "paid",
        *([Sales.commissioner_id == actor.id] if restrict_to_commissioner else []),
    ).group_by(Product.name).all()

    sales_by_day_raw = db.query(
        func.date(Sales.sale_date),
        func.count(Sales.id)
    ).join(Product).join(Event).filter(
        Event.id == event_id,
        Sales.status == SaleStatus.paid,
        *([Sales.commissioner_id == actor.id] if restrict_to_commissioner else []),
    ).group_by(
        func.date(Sales.sale_date)
    ).order_by(
        func.date(Sales.sale_date).asc()
    ).limit(30).all()

    # Taxa de cancelamento
    cancellation_rate = (total_canceled_sales / (total_paid_sales + total_canceled_sales)) if (total_paid_sales + total_canceled_sales) > 0 else 0.0

    ## Formatar os resultados para o modelo de resposta
    sales_by_product = [{"product_name": name, "sales_count": count} for name, count in sales_by_product_raw]
    sales_by_day = [{"sale_date": date, "sales_count": count} for date, count in sales_by_day_raw]

    return DashboardResponse(
        total_paid_sales=total_paid_sales,
        total_canceled_sales=total_canceled_sales,
        total_checkins=total_checkins,
        total_revenue=total_revenue,
        average_ticket=average_ticket,
        checkin_rate=checkin_rate,
        sales_by_product=sales_by_product,
        sales_by_day=sales_by_day,
        cancellation_rate=cancellation_rate,
    )