from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.product_group import ProductGroup, ProductGroupMembership
from models.products import Product
from models.event import Event
from models.user import User
from schemas.product_group import ProductGroupCreate, ProductGroupUpdate

if TYPE_CHECKING:
    from models.commissioner import Commissioner

EventManager = User  # alias — o tipo real é Union[User, Commissioner]


def _check_event_access(db: Session, event_id: int, principal: EventManager) -> Event:
    from models.commissioner import Commissioner
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    if isinstance(principal, Commissioner):
        # Commissioner com full_access já foi validado na dependency;
        # aqui verificamos apenas se pertence ao evento correto.
        if principal.event_id != event_id:
            raise HTTPException(status_code=403, detail="Acesso negado")
    else:
        if principal.role != "admin" and event.user_id != principal.id:
            raise HTTPException(status_code=403, detail="Acesso negado")

    return event


def _get_group_or_404(db: Session, event_id: int, group_id: int) -> ProductGroup:
    group = db.query(ProductGroup).filter(
        ProductGroup.id == group_id,
        ProductGroup.event_id == event_id,
    ).first()
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    return group


# ---------------------------------------------------------------------------
# CRUD de grupos
# ---------------------------------------------------------------------------

def create_group(db: Session, event_id: int, data: ProductGroupCreate, current_user: User) -> ProductGroup:
    _check_event_access(db, event_id, current_user)

    if data.is_default:
        existing_default = db.query(ProductGroup).filter(
            ProductGroup.event_id == event_id,
            ProductGroup.is_default == True,
        ).first()
        if existing_default:
            raise HTTPException(status_code=400, detail="Já existe um grupo padrão para este evento")

    if data.parent_group_id is not None:
        parent = db.query(ProductGroup).filter(
            ProductGroup.id == data.parent_group_id,
            ProductGroup.event_id == event_id,
        ).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Grupo pai não encontrado neste evento")

    group = ProductGroup(
        name=data.name,
        event_id=event_id,
        parent_group_id=data.parent_group_id,
        is_default=data.is_default,
    )
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def get_groups(db: Session, event_id: int, current_user: User) -> list[ProductGroup]:
    _check_event_access(db, event_id, current_user)
    # Retorna apenas raízes; children são carregados via relationship
    return db.query(ProductGroup).filter(
        ProductGroup.event_id == event_id,
        ProductGroup.parent_group_id == None,
    ).all()


def get_group_by_id(db: Session, event_id: int, group_id: int, current_user: User) -> ProductGroup:
    _check_event_access(db, event_id, current_user)
    return _get_group_or_404(db, event_id, group_id)


def update_group(db: Session, event_id: int, group_id: int, data: ProductGroupUpdate, current_user: User) -> ProductGroup:
    _check_event_access(db, event_id, current_user)
    group = _get_group_or_404(db, event_id, group_id)

    if data.is_default is True and not group.is_default:
        existing_default = db.query(ProductGroup).filter(
            ProductGroup.event_id == event_id,
            ProductGroup.is_default == True,
        ).first()
        if existing_default:
            raise HTTPException(status_code=400, detail="Já existe um grupo padrão para este evento")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(group, key, value)

    db.commit()
    db.refresh(group)
    return group


def delete_group(db: Session, event_id: int, group_id: int, current_user: User) -> None:
    _check_event_access(db, event_id, current_user)
    group = _get_group_or_404(db, event_id, group_id)

    if group.children:
        raise HTTPException(status_code=400, detail="Remova os subgrupos antes de excluir o grupo pai")

    db.delete(group)
    db.commit()


# ---------------------------------------------------------------------------
# Gestão de memberships (produto ↔ grupo)
# ---------------------------------------------------------------------------

def add_product_to_group(db: Session, event_id: int, group_id: int, product_id: int, current_user: User) -> ProductGroupMembership:
    _check_event_access(db, event_id, current_user)
    _get_group_or_404(db, event_id, group_id)

    product = db.query(Product).filter(Product.id == product_id, Product.event_id == event_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado neste evento")

    existing = db.query(ProductGroupMembership).filter(
        ProductGroupMembership.product_id == product_id,
        ProductGroupMembership.group_id == group_id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Produto já está neste grupo")

    membership = ProductGroupMembership(product_id=product_id, group_id=group_id)
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


def toggle_product_in_group(
    db: Session, event_id: int, group_id: int, product_id: int, is_active: bool, current_user: User
) -> ProductGroupMembership:
    _check_event_access(db, event_id, current_user)
    _get_group_or_404(db, event_id, group_id)

    membership = db.query(ProductGroupMembership).filter(
        ProductGroupMembership.product_id == product_id,
        ProductGroupMembership.group_id == group_id,
    ).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Produto não está neste grupo")

    membership.is_active = is_active
    db.commit()
    db.refresh(membership)
    return membership


def remove_product_from_group(db: Session, event_id: int, group_id: int, product_id: int, current_user: User) -> None:
    _check_event_access(db, event_id, current_user)
    _get_group_or_404(db, event_id, group_id)

    membership = db.query(ProductGroupMembership).filter(
        ProductGroupMembership.product_id == product_id,
        ProductGroupMembership.group_id == group_id,
    ).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Produto não está neste grupo")

    db.delete(membership)
    db.commit()
