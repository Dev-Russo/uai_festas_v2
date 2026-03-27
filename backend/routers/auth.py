from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.schemas.user import UserCreate, UserResponse, Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    from backend.services.user import register_user
    return register_user(db, user)

@router.post("/login", response_model=Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    from backend.services.user import login_user
    return login_user(db, user)