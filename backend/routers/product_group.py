from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from dependencies.db import get_db
from schemas.product_group import (
    ProductGroupCreate,
    ProductGroupUpdate,
    ProductGroupResponse,
    MembershipResponse,
    MembershipToggle,
)
from utils.security import get_current_event_manager

router = APIRouter(prefix="/events/{event_id}/product-groups", tags=["product-groups"])


@router.post("/", response_model=ProductGroupResponse, status_code=status.HTTP_201_CREATED)
def create(event_id: int, data: ProductGroupCreate, db: Session = Depends(get_db), principal=Depends(get_current_event_manager)):
    from services.product_group import create_group
    return create_group(db, event_id, data, principal)


@router.get("/", response_model=list[ProductGroupResponse])
def list_groups(event_id: int, db: Session = Depends(get_db), principal=Depends(get_current_event_manager)):
    from services.product_group import get_groups
    return get_groups(db, event_id, principal)


@router.get("/{group_id}", response_model=ProductGroupResponse)
def get_one(event_id: int, group_id: int, db: Session = Depends(get_db), principal=Depends(get_current_event_manager)):
    from services.product_group import get_group_by_id
    return get_group_by_id(db, event_id, group_id, principal)


@router.patch("/{group_id}", response_model=ProductGroupResponse)
def update(event_id: int, group_id: int, data: ProductGroupUpdate, db: Session = Depends(get_db), principal=Depends(get_current_event_manager)):
    from services.product_group import update_group
    return update_group(db, event_id, group_id, data, principal)


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(event_id: int, group_id: int, db: Session = Depends(get_db), principal=Depends(get_current_event_manager)):
    from services.product_group import delete_group
    delete_group(db, event_id, group_id, principal)


@router.post("/{group_id}/products", response_model=MembershipResponse, status_code=status.HTTP_201_CREATED)
def add_product(event_id: int, group_id: int, product_id: int, db: Session = Depends(get_db), principal=Depends(get_current_event_manager)):
    from services.product_group import add_product_to_group
    return add_product_to_group(db, event_id, group_id, product_id, principal)


@router.patch("/{group_id}/products/{product_id}", response_model=MembershipResponse)
def toggle_product(event_id: int, group_id: int, product_id: int, data: MembershipToggle, db: Session = Depends(get_db), principal=Depends(get_current_event_manager)):
    from services.product_group import toggle_product_in_group
    return toggle_product_in_group(db, event_id, group_id, product_id, data.is_active, principal)


@router.delete("/{group_id}/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_product(event_id: int, group_id: int, product_id: int, db: Session = Depends(get_db), principal=Depends(get_current_event_manager)):
    from services.product_group import remove_product_from_group
    remove_product_from_group(db, event_id, group_id, product_id, principal)
