from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.utils.security import get_current_user
from backend.models.user import User
from backend.schemas.user import UserCreate, UserLogin, UserResponse, Token

router = APIRouter(prefix='/users', tags=['users'])

@router.get('/me', response_model=UserResponse)
def get_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> User:

    user = db.query(User).filter(User.name == current_user.name).first()
    if not user:
        raise HTTPException(status_code= 404, detail= "User Not Found")
    
    return user