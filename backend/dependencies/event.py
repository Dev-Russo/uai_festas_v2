from fastapi import Depends, HTTPException, Path
from sqlalchemy.orm import Session
from models.event import Event
from models.user import User
from utils.security import get_current_user
from dependencies.db import get_db

def get_event_by_id(
    event_id: int = Path(..., title="ID do evento"),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
) -> Event:
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    # Permissão: só o dono ou admin pode acessar
    if user.role != "admin" and event.owner.id != user.id:
        raise HTTPException(status_code=403, detail="Você não é dono desse evento")
    return event