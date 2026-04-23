from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models.commissioner import Commissioner
from models.event import Event
from models.user import User
from schemas.commissioner import CommissionerCreate, CommissionerUpdate
from utils.security import get_password_hash

def create_commissioner(db: Session, event_id: int, data: CommissionerCreate, current_user: User) -> Commissioner:
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    if current_user.role != "admin" and event.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    existing = db.query(Commissioner).filter(Commissioner.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username já está em uso")

    commissioner = Commissioner(
        username=data.username,
        name=data.name,
        hashed_password=get_password_hash(data.password),
        event_id=event_id,
        role=data.role,
        full_access=data.full_access,
        is_active=data.is_active,
    )
    db.add(commissioner)
    try:
        db.commit()
        db.refresh(commissioner)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username já está em uso")
    return commissioner

def get_commissioners(db: Session, event_id: int, current_user: User) -> list[Commissioner]:
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    if current_user.role != "admin" and event.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return db.query(Commissioner).filter(Commissioner.event_id == event_id).all()

def get_commissioner_by_id(db: Session, event_id: int, commissioner_id: int, current_user: User) -> Commissioner:
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    if current_user.role != "admin" and event.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    commissioner = db.query(Commissioner).filter(
        Commissioner.id == commissioner_id,
        Commissioner.event_id == event_id,
    ).first()
    if not commissioner:
        raise HTTPException(status_code=404, detail="Comissário não encontrado")
    return commissioner

def update_commissioner(
    db: Session, event_id: int, commissioner_id: int, data: CommissionerUpdate, current_user: User
) -> Commissioner:
    commissioner = get_commissioner_by_id(db, event_id, commissioner_id, current_user)
    update_data = data.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    for key, value in update_data.items():
        setattr(commissioner, key, value)
    try:
        db.commit()
        db.refresh(commissioner)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username já está em uso")
    return commissioner

def delete_commissioner(db: Session, event_id: int, commissioner_id: int, current_user: User) -> None:
    commissioner = get_commissioner_by_id(db, event_id, commissioner_id, current_user)
    db.delete(commissioner)
    db.commit()
