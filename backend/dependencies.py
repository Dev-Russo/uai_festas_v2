from backend.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Path
from backend.models.event import Event
from backend.models.user import User

"""
    This function is a dependency that provides a database session to the routes that require it. It creates a new session using the SessionLocal class from the database module, yields it to the caller, and then closes the session after the request is completed. This allows us to use the same session for multiple requests without having to create a new one for each request, which can improve performance and reduce resource usage. By using this dependency in our routes, we can easily access the database and perform CRUD operations on our models without having to worry about managing the database connection ourselves.
"""

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependência para buscar evento pelo event_id da rota e garantir permissão
def get_event_by_id(
    event_id: int = Path(..., title="ID do evento"),
    db: Session = Depends(get_db),
    user: User = Depends("get_current_user")
) -> Event:
    
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    # Permissão: só o dono ou admin pode acessar
    if user.role != "admin" and event.owner.id != user.id:
        raise HTTPException(status_code=403, detail="Você não é dono desse evento")
    return event