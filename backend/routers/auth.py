from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils import security
from backend import database
from backend.models import User
from backend.schemas import UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserCreate)
def register(user: UserCreate, db: Session = Depends(database.get_db)) -> User:

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = security.get_password_hash(user.hashed_password)
    new_user = User(name=user.name, email=user.email, role=user.role, is_active=user.is_active, hashed_password=hashed_password)
    db.add(new_user)
    
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(database.get_db)) -> str:

    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not security.verify_password(user.hashed_password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = security.create_access_token(
        data={
            "sub": db_user.email, 
            "role": db_user.role
        }
    )

    return {"access_token": access_token, "token_type": "bearer"}