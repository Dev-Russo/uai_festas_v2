from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.models.user import User, Event
from fastapi import HTTPException

def create_event(db: Session, event_data: dict, user: User):
    from backend.models.event import Event

    new_event = Event(**event_data, owner=user)

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event

def update_event(db: Session, event: Event, user: User, event_data: dict):
    for key, value in event_data.items():
        setattr(event, key, value)

    if user.id != event.owner.id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    db.commit()
    db.refresh(event)

    return event

def get_events(db: Session, user: User):
    query_event = db.query(Event).filter(Event.user_id == user.id).all()
    if not query_event:
        raise HTTPException(status_code=404, detail="Nenhum evento encontrado")
    if query_event.owner.id != user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return query_event

def get_event_by_id(db: Session, event_id: int, user: User):
    event = db.query(Event).filter(Event.id == event_id, Event.user_id == user.id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    if event.owner.id != user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    return event

def delete_event(db: Session, user: User, event: Event):
    if event.owner.id != user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    event.status = "Cancelado"
    db.commit()
    db.refresh(event)
