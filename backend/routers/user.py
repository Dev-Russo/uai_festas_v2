from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.dependencies import get_db
from backend.utils.security import get_current_user
from backend.models.user import User
from backend.schemas.user import UserResponse, UserUpdate, PasswordChange

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/me', response_model=UserResponse)
def get_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> UserResponse:
    from backend.services.user import get_user_profile
    return get_user_profile(db, current_user)

@router.put('/me', response_model=UserResponse)
def edit_user(user_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> UserResponse:
    from backend.services.user import update_user_profile
    return update_user_profile(db, current_user, user_data)

@router.put('/me/change-password', response_model=UserResponse)
def change_password(
    
    data: PasswordChange, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    
    ):
    
    from backend.services.user import update_user_password
    return update_user_password(db, current_user, data)