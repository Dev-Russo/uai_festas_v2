from fastapi import HTTPException
from enums.user import UserRole
from models.sales import Sales
from models.user import User
from models.products import Product
from models.event import Event
from schemas.sales import SalesCreate, SalesUpdate, SalesResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone


def create_sale(db: Session, current_user: User, sale: SalesCreate, event_id: int) -> SalesResponse:
    if current_user.role != UserRole.admin and current_user.role != UserRole.producer:
        raise HTTPException(status_code=403, detail="Acesso negado")

    # Buscar produto
    product = db.query(Product).filter(Product.id == sale.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Buscar evento
    event = db.query(Event).filter(Event.id == product.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    if product.event_id != event_id:
        raise HTTPException(status_code=400, detail="Produto nao pertence ao evento informado")

    # Preço vem do produto
    db_sale = Sales(
        buyer_name=sale.buyer_name,
        buyer_email=sale.buyer_email,
        product_id=sale.product_id,
        method_of_payment=sale.method_of_payment,
        sale_date=sale.sale_date,
        status=sale.status,
        price=product.price
    )
    
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)

    return db_sale

def get_sales(db: Session, current_user: User, event_id: int) -> SalesResponse:
    if current_user.role == UserRole.admin:
        sales = db.query(Sales).join(Sales.product).filter(Product.event_id == event_id).all()

    elif current_user.role == UserRole.producer:
        sales = db.query(Sales).join(Sales.product).filter(Product.event_id == event_id).all()

    else:
        sales = (
            db.query(Sales)
            .join(Sales.product)
            .filter(Sales.buyer_email == current_user.email, Product.event_id == event_id)
            .all()
        )

    return sales

def get_sale_by_id(db: Session, current_user: User, sale_id: int, event_id: int) -> SalesResponse:
    if current_user.role == UserRole.admin:
        sale = (
            db.query(Sales)
            .join(Sales.product)
            .filter(Sales.id == sale_id, Product.event_id == event_id)
            .first()
        )
    elif current_user.role == UserRole.producer:
        sale = (
            db.query(Sales)
            .join(Sales.product)
            .filter(Sales.id == sale_id, Product.event_id == event_id)
            .first()
        )
    else:
        sale = (
            db.query(Sales)
            .join(Sales.product)
            .filter(Sales.id == sale_id, Sales.buyer_email == current_user.email, Product.event_id == event_id)
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

def cancel_sale(db: Session, current_user: User, sale_id: int, event_id: int) -> SalesResponse:
    if current_user.role != UserRole.admin and current_user.role != UserRole.producer:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
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

def check_in_sale(db: Session, current_user: User, sale_id: int, event_id: int) -> SalesResponse:
    if current_user.role != UserRole.admin and current_user.role != UserRole.producer:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
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