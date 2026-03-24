from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.utils.security import get_current_user
from backend.models.user import User
from backend.schemas.event import EventCreate, EventUpdate, EventResponse

router = APIRouter(prefix='/events', tags=['events'])

@router.post('/', response_model=EventResponse)
def create_event(event_data: EventCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    from backend.services.events import create_event
    return create_event(db, event_data, current_user)

@router.put('/{event_id}', response_model=EventResponse)
def update_event(event_id: int, event_data: EventUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    from backend.services.events import get_event_by_id, update_event
    event = get_event_by_id(db, event_id, current_user)
    return update_event(db, event, current_user, event_data)

@router.get('/', response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    from backend.services.events import get_events
    return get_events(db, current_user)

@router.get('/{event_id}', response_model=EventResponse)
def get_event_by_id(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    from backend.services.events import get_event_by_id
    return get_event_by_id(db, event_id, current_user)

@router.delete('/{event_id}', response_model=EventResponse)
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    from backend.services.events import get_event_by_id, delete_event
    event = get_event_by_id(db, event_id, current_user)
    return delete_event(db, current_user, event)