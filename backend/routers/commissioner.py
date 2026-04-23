from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from dependencies.db import get_db
from models.user import User
from models.commissioner import Commissioner
from schemas.commissioner import CommissionerCreate, CommissionerUpdate, CommissionerResponse
from utils.security import get_current_user, get_current_commissioner

# Rota de self-service do comissário (sem event_id na URL)
me_router = APIRouter(prefix="/commissioners", tags=["commissioners"])

@me_router.get("/me", response_model=CommissionerResponse)
def get_me(commissioner: Commissioner = Depends(get_current_commissioner)):
    return commissioner

# Rotas de gestão (admin/produtor, nested sob evento)
router = APIRouter(prefix="/events/{event_id}/commissioners", tags=["commissioners"])

@router.post("/", response_model=CommissionerResponse, status_code=status.HTTP_201_CREATED)
def create(event_id: int, data: CommissionerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from services.commissioner import create_commissioner
    return create_commissioner(db, event_id, data, current_user)

@router.get("/", response_model=list[CommissionerResponse])
def list_commissioners(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from services.commissioner import get_commissioners
    return get_commissioners(db, event_id, current_user)

@router.get("/{commissioner_id}", response_model=CommissionerResponse)
def get_one(event_id: int, commissioner_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from services.commissioner import get_commissioner_by_id
    return get_commissioner_by_id(db, event_id, commissioner_id, current_user)

@router.patch("/{commissioner_id}", response_model=CommissionerResponse)
def update(event_id: int, commissioner_id: int, data: CommissionerUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from services.commissioner import update_commissioner
    return update_commissioner(db, event_id, commissioner_id, data, current_user)

@router.delete("/{commissioner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(event_id: int, commissioner_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from services.commissioner import delete_commissioner
    delete_commissioner(db, event_id, commissioner_id, current_user)
