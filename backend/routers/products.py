from fastapi import APIRouter, Depends, HTTPException
from dependencies.event import get_event_by_id
from sqlalchemy.orm import Session
from dependencies import get_db
from utils.security import get_current_user, get_current_actor
from models.user import User
from models.event import Event
from schemas.event import EventCreate, EventUpdate, EventResponse
from schemas.products import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/events/{event_id}/products", tags=["products"])

@router.post("/", response_model=ProductResponse)
def create_products(
    product_data: ProductCreate, 
    event: Event = Depends(get_event_by_id), 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
    ):
    
    from services.products import create_product
    return create_product(db, product_data, event, user)

@router.put("/{id_product}", response_model=ProductResponse)
def update_products(
    id_product: int,
    product_data: ProductUpdate,
    event: Event = Depends(get_event_by_id),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)

):
    from services.products import update_product, get_product_by_id
    product = get_product_by_id(db, user, event, id_product)
    return update_product(db, product, product_data, event, user)

@router.get("/", response_model=list[ProductResponse])
def get_products(
    event_id: int,
    db: Session = Depends(get_db),
    actor=Depends(get_current_actor),
):
    from models.commissioner import Commissioner
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    if isinstance(actor, Commissioner):
        if actor.event_id != event_id:
            raise HTTPException(status_code=403, detail="Acesso negado a este evento")
    elif actor.role != "admin" and event.owner.id != actor.id:
        raise HTTPException(status_code=403, detail="Você não é dono desse evento")
    from services.products import get_products
    return get_products(db, actor, event)

@router.get("/{id_product}", response_model=ProductResponse)
def get_product_by_id(
    id_product: int,
    event: Event = Depends(get_event_by_id),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    from services.products import get_product_by_id
    return get_product_by_id(db, user, event, id_product)

@router.delete("/{id_product}", response_model=ProductResponse)
def delete_product(
    id_product: int,
    event: Event = Depends(get_event_by_id),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    from services.products import delete_product
    return delete_product(db, user, event, id_product)