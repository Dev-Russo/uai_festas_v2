from dependencies.db import get_db
from models.sales import Sales
from models.user import User
from models.products import Product
from models.event import Event
from schemas.sales import SalesCreate, SalesUpdate, SalesResponse, EmailRequest
from sqlalchemy.orm import Session
from services.events import get_event_by_id
from utils.security import get_current_user, get_current_actor, get_current_event_manager
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from fastapi import HTTPException
from io import BytesIO
from datetime import datetime

router = APIRouter(prefix="/events/{event_id}/sales", tags=["sales"])

@router.post("/", response_model=SalesResponse)
def create_sale(
    event_id: int,
    sale: SalesCreate,
    db: Session = Depends(get_db),
    actor=Depends(get_current_actor),
) -> SalesResponse:
    from services.sales import create_sale
    return create_sale(db, actor, sale, event_id)

@router.get("/", response_model=list[SalesResponse])
def get_sales(
    event_id: int,
    db: Session = Depends(get_db),
    actor=Depends(get_current_actor),
) -> list[SalesResponse]:
    from services.sales import get_sales
    return get_sales(db, actor, event_id)

@router.get("/{sale_id}", response_model=SalesResponse)
def get_sale_by_id(
    event_id: int,
    sale_id: int,
    db: Session = Depends(get_db),
    actor=Depends(get_current_actor),
) -> SalesResponse:
    from services.sales import get_sale_by_id
    return get_sale_by_id(db, actor, sale_id, event_id)

@router.put("/{sale_id}", response_model=SalesResponse)
def update_sale(
    sale_id: int,
    sale_data: SalesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SalesResponse:
    from services.sales import update_sale
    return update_sale(db, current_user, sale_id, sale_data)

@router.delete("/{sale_id}")
def delete_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from services.sales import delete_sale
    return delete_sale(db, current_user, sale_id)

@router.patch("/{sale_id}/check-in", response_model=SalesResponse)
def check_in_sale(
    event_id: int,
    sale_id: int,
    db: Session = Depends(get_db),
    manager=Depends(get_current_event_manager),
) -> SalesResponse:
    from services.sales import check_in_sale
    return check_in_sale(db, manager, sale_id, event_id)

@router.patch("/{sale_id}/cancel", response_model=SalesResponse)
def cancel_sale(
    event_id: int,
    sale_id: int,
    db: Session = Depends(get_db),
    manager=Depends(get_current_event_manager),
) -> SalesResponse:
    from services.sales import cancel_sale
    return cancel_sale(db, manager, sale_id, event_id)


@router.get("/{sale_id}/ticket")
def get_ticket_pdf(
    event_id: int,
    sale_id: int,
    db: Session = Depends(get_db),
    actor=Depends(get_current_actor),
):
    from services.ticket import generate_qr_png_bytes, generate_ticket_pdf_bytes
    sale = db.query(Sales).join(Sales.product).filter(Sales.id == sale_id, Product.event_id == event_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

    product = sale.product
    event = db.query(Event).filter(Event.id == product.event_id).first()

    qr = generate_qr_png_bytes(str(sale.unique_code))
    pdf = generate_ticket_pdf_bytes(sale, product, event, qr)

    return StreamingResponse(BytesIO(pdf), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=receipt_{sale.id}.pdf"})


@router.post("/{sale_id}/email")
def send_ticket_by_email(
    event_id: int,
    sale_id: int,
    payload: EmailRequest,
    db: Session = Depends(get_db),
    actor=Depends(get_current_actor),
):
    from services.email_service import send_email_with_attachment
    from services.ticket import generate_qr_png_bytes, generate_ticket_pdf_bytes

    sale = db.query(Sales).join(Sales.product).filter(Sales.id == sale_id, Product.event_id == event_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

    product = sale.product
    event = db.query(Event).filter(Event.id == product.event_id).first()

    qr = generate_qr_png_bytes(str(sale.unique_code))
    pdf = generate_ticket_pdf_bytes(sale, product, event, qr)

    to_email = payload.to_email if payload.to_email else sale.buyer_email
    subject = payload.subject or f"Ticket - {event.name}"
    body = payload.body or "Segue o ingresso em anexo."

    send_email_with_attachment(to_email, subject, body, pdf, f"ticket_{sale.id}.pdf")

    return {"status": "sent"}


# Lookup ticket by unique code (useful for scanner apps)
@router.get("/tickets/{unique_code}")
def get_ticket_by_code(
    unique_code: str,
    db: Session = Depends(get_db),
    actor=Depends(get_current_actor),
):
    sale = db.query(Sales).filter(Sales.unique_code == unique_code).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Ingresso não encontrado")

    product = sale.product
    event = db.query(Event).filter(Event.id == product.event_id).first()

    return {
        "sale_id": sale.id,
        "event_id": event.id if event else None,
        "product_id": product.id if product else None,
        "buyer_name": sale.buyer_name,
        "buyer_cpf": sale.buyer_cpf,
        "status": sale.status,
        "checkin_at": sale.checkin_at.isoformat() if sale.checkin_at else None,
        "unique_code": str(sale.unique_code),
    }


# Check-in by unique code (requires event manager / commissioner full access)
@router.post("/tickets/{unique_code}/check-in")
def check_in_by_code(
    unique_code: str,
    db: Session = Depends(get_db),
    manager=Depends(get_current_event_manager),
):
    sale = db.query(Sales).filter(Sales.unique_code == unique_code).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Ingresso não encontrado")
    if sale.checkin_at is not None:
        raise HTTPException(status_code=400, detail="Ingresso já validado/check-in realizado")

    sale.checkin_at = datetime.utcnow()
    db.add(sale)
    db.commit()
    db.refresh(sale)

    return {"status": "ok", "sale_id": sale.id, "checkin_at": sale.checkin_at.isoformat()}
