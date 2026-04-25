from fastapi import HTTPException
from enums.user import UserRole
from models.sales import Sales
from models.user import User
from models.products import Product
from models.event import Event
from schemas.sales import SalesCreate, SalesUpdate, SalesResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone


def create_sale(db: Session, actor, sale: SalesCreate, event_id: int) -> SalesResponse:
    from models.commissioner import Commissioner
    if not isinstance(actor, Commissioner):
        if actor.role != UserRole.admin and actor.role != UserRole.producer:
            raise HTTPException(status_code=403, detail="Acesso negado")

    product = db.query(Product).filter(Product.id == sale.product_id).with_for_update().first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    event = db.query(Event).filter(Event.id == product.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    if product.event_id != event_id:
        raise HTTPException(status_code=400, detail="Produto nao pertence ao evento informado")

    if product.available_quantity is not None and product.available_quantity <= 0:
        raise HTTPException(status_code=400, detail="Produto esgotado")

    from models.commissioner import Commissioner
    commissioner_id = actor.id if isinstance(actor, Commissioner) else None

    db_sale = Sales(
        buyer_name=sale.buyer_name,
        buyer_email=sale.buyer_email,
        product_id=sale.product_id,
        method_of_payment=sale.method_of_payment,
        sale_date=sale.sale_date,
        status=sale.status,
        price=product.price,
        commissioner_id=commissioner_id,
    )
    
    if product.available_quantity is not None:
        product.available_quantity -= 1

    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)

    return db_sale

def get_sales(db: Session, actor, event_id: int) -> list:
    from models.commissioner import Commissioner
    query = db.query(Sales).join(Sales.product).filter(Product.event_id == event_id)
    if isinstance(actor, Commissioner) and not actor.full_access:
        query = query.filter(Sales.commissioner_id == actor.id)
    return query.all()

def get_sale_by_id(db: Session, actor, sale_id: int, event_id: int) -> SalesResponse:
    sale = (
        db.query(Sales)
        .join(Sales.product)
        .filter(Sales.id == sale_id, Product.event_id == event_id)
        .first()
    )
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return sale

def update_sale(db: Session, current_user: User, sale_id: int, sale_data: SalesUpdate) -> SalesResponse:
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    sale = db.query(Sales).filter(Sales.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    for key, value in sale_data.model_dump(exclude_unset=True).items():
        setattr(sale, key, value)

    db.commit()
    db.refresh(sale)

    return sale

def cancel_sale(db: Session, manager, sale_id: int, event_id: int) -> SalesResponse:
    # authorization already validated by get_current_event_manager in the router
    sale = (
        db.query(Sales)
        .join(Sales.product)
        .filter(Sales.id == sale_id, Product.event_id == event_id)
        .first()
    )
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

    sale.status = "cancelled"
    db.commit()
    db.refresh(sale)

    return sale

def check_in_sale(db: Session, manager, sale_id: int, event_id: int) -> SalesResponse:
    # authorization already validated by get_current_event_manager in the router
    sale = (
        db.query(Sales)
        .join(Sales.product)
        .filter(Sales.id == sale_id, Product.event_id == event_id)
        .first()
    )
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

    # Check-in agora e um timestamp. O status da venda nao deve ser alterado.
    if sale.status == "cancelled":
        raise HTTPException(status_code=400, detail="Nao e possivel fazer check-in de venda cancelada")
    
    if sale.checkin_at is not None:
        raise HTTPException(status_code=400, detail="Venda ja foi check-in")

    sale.checkin_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(sale)

    return sale

def delete_sale(db: Session, current_user: User, sale_id: int) -> SalesResponse:
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    sale = db.query(Sales).filter(Sales.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    db.delete(sale)
    db.commit()

    return sale