from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_db
from schemas.user import TokenData
from models.user import User
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password) -> str:
    return pwd_context.hash(password[:72])

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        email: str = payload.get("sub")
        user_type: str = payload.get("user_type", "user")
        if email is None or user_type != "user":
            raise credentials_exception
        token_data = TokenData(email=email, role=payload.get("role"), user_type=user_type)
    except Exception:
        raise credentials_exception

    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_event_manager(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Retorna User (dono/admin) ou Commissioner com full_access. Usado em rotas de gestão do evento."""
    from models.commissioner import Commissioner
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        sub: str = payload.get("sub")
        user_type: str = payload.get("user_type", "user")
        if sub is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    if user_type == "user":
        user = db.query(User).filter(User.email == sub).first()
        if user is None:
            raise credentials_exception
        return user

    if user_type == "commissioner":
        commissioner = db.query(Commissioner).filter(Commissioner.username == sub).first()
        if commissioner is None or not commissioner.is_active:
            raise credentials_exception
        if not commissioner.full_access:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
        return commissioner

    raise credentials_exception


def get_current_commissioner(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from models.commissioner import Commissioner
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username: str = payload.get("sub")
        user_type: str = payload.get("user_type", "user")
        if username is None or user_type != "commissioner":
            raise credentials_exception
    except Exception:
        raise credentials_exception

    commissioner = db.query(Commissioner).filter(Commissioner.username == username).first()
    if commissioner is None or not commissioner.is_active:
        raise credentials_exception
    return commissioner
