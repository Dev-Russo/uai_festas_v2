from dependencies.db import get_db
from models.sales import Sales
from models.user import User
from models.products import Product
from models.event import Event
from schemas.sales import SalesCreate, SalesUpdate, SalesResponse
from sqlalchemy.orm import Session
from services.events import get_event_by_id
from utils.security import get_current_user, get_current_actor, get_current_event_manager
from fastapi import APIRouter, Depends

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
