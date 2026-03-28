from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies.db import get_db
from utils.security import get_current_user
from dependencies.event import get_event_by_id as event_dep_get_event_by_id
from models.user import User
from schemas.event import EventCreate, EventUpdate, EventResponse

router = APIRouter(prefix='/events', tags=['events'])

@router.post('/', response_model=EventResponse)
def create_event(event_data: EventCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    from services.events import create_event
    return create_event(db, event_data, current_user)

@router.put('/{event_id}', response_model=EventResponse)
def update_event(event_id: int, event_data: EventUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from services.events import update_event
    event = event_dep_get_event_by_id(event_id, db, current_user)
    return update_event(db, event, current_user, event_data)

@router.get('/', response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    from services.events import get_events
    return get_events(db, current_user)

@router.get('/{event_id}', response_model=EventResponse)
def get_event_by_id_route(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = event_dep_get_event_by_id(event_id, db, current_user)
    return event

@router.delete('/{event_id}', response_model=EventResponse)
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from services.events import delete_event
    event = event_dep_get_event_by_id(event_id, db, current_user)
    return delete_event(db, event, current_user)