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

"""Security utilities for password hashing and verification using bcrypt algorithm."""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""Functions for hashing and verifying passwords."""
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

"""Function to hash a password using bcrypt algorithm."""
def get_password_hash(password) -> str:
    print("Senha recebida para hash:", password, "Tamanho:", len(password))
    return pwd_context.hash(password[:72])

"""Function to create a JWT access token with an expiration time."""
def create_access_token(data: dict) -> str:
    ## Claims to be encoded in the JWT token, including the expiration time.
    to_encode = data.copy()
    ## Summ the current UTC time with the configured token expiration time to set the "exp" claim.
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    ## Update the claims to be encoded with the expiration time.
    to_encode.update({"exp": expire})

    ## Encode the claims into a JWT token using the secret key and the HS256 algorithm.
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, key = settings.SECRET_KEY, algorithms = settings.ALGORITHM)
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
        else:
            token_data = TokenData(email = email)
    except:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user