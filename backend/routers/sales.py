from backend.dependencies.db import get_db
from backend.models.sales import Sales
from backend.models.user import User
from backend.models.products import Product
from backend.models.event import Event
from backend.schemas.sales import SalesCreate, SalesUpdate, SalesResponse
from sqlalchemy.orm import Session
from backend.services.events import get_event_by_id
from backend.utils.security import get_current_user
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/event/{event_id}/sales", tags=["sales"])

@router.post("/", response_model=SalesResponse)
def create_sale(
    event_id: int,
    sale: SalesCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    
    
) -> SalesResponse:
    
    from backend.services.sales import create_sale
    return create_sale(db, current_user, sale)

@router.get("/", response_model=list[SalesResponse])
def get_sales(
    event_id: int,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
) -> list[SalesResponse]:
    
    from backend.services.sales import get_sales
    return get_sales(db, current_user)

@router.get("/{sale_id}", response_model=SalesResponse)
def get_sale_by_id(
    sale_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
) -> SalesResponse:
    
    from backend.services.sales import get_sale_by_id
    return get_sale_by_id(db, current_user, sale_id)

@router.put("/{sale_id}", response_model=SalesResponse)
def update_sale(
    sale_id: int, 
    sale_data: SalesUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
) -> SalesResponse:
    
    from backend.services.sales import update_sale
    return update_sale(db, current_user, sale_id, sale_data)

@router.delete("/{sale_id}")
def delete_sale(
    sale_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    
    from backend.services.sales import delete_sale
    return delete_sale(db, current_user, sale_id)

@router.patch("/{sale_id}/check-in", response_model=SalesResponse)
def check_in_sale(
    sale_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
) -> SalesResponse:
    
    from backend.services.sales import check_in_sale
    return check_in_sale(db, current_user, sale_id)

@router.patch("/{sale_id}/cancel", response_model=SalesResponse)
def cancel_sale(
    sale_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
) -> SalesResponse:
    
    from backend.services.sales import cancel_sale
    return cancel_sale(db, current_user, sale_id)
