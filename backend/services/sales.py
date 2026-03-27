from fastapi import HTTPException
from backend.enums.user import UserRole
from backend.models.sales import Sales
from backend.models.user import User
from backend.models.products import Product
from backend.models.event import Event
from backend.schemas.sales import SalesCreate, SalesUpdate, SalesResponse
from sqlalchemy.orm import Session


def create_sale(db: Session, current_user: User, sale: SalesCreate) -> SalesResponse:
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

def get_sales(db: Session, current_user: User) -> SalesResponse:
    if current_user.role == UserRole.admin:
        sales = db.query(Sales).all()

    elif current_user.role == UserRole.producer:
        sales = db.query(Sales).join(Sales.product).join(Product.event).filter(Event.user_id == current_user.id).all()

    else:
        sales = db.query(Sales).filter(Sales.buyer_email == current_user.email).all()

    return sales

def get_sale_by_id(db: Session, current_user: User, sale_id: int) -> SalesResponse:
    if current_user.role == UserRole.admin:
        sale = db.query(Sales).filter(Sales.id == sale_id).first()
    elif current_user.role == UserRole.producer:
        sale = db.query(Sales).join(Sales.product).join(Product.event).filter(Sales.id == sale_id, Event.user_id == current_user.id).first()
    else:
        sale = db.query(Sales).filter(Sales.id == sale_id, Sales.buyer_email == current_user.email).first()

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

def cancel_sale(db: Session, current_user: User, sale_id: int) -> SalesResponse:
    if current_user.role != UserRole.admin and current_user.role != UserRole.producer:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    sale = db.query(Sales).filter(Sales.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    sale.status = "cancelled"
    db.commit()
    db.refresh(sale)

    return sale

def check_in_sale(db: Session, current_user: User, sale_id: int) -> SalesResponse:
    if current_user.role != UserRole.admin and current_user.role != UserRole.producer:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    sale = db.query(Sales).filter(Sales.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    
    sale.status = "check_in"
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