from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from backend.config import settings

"""Security utilities for password hashing and verification using bcrypt algorithm."""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""Functions for hashing and verifying passwords."""
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

"""Function to hash a password using bcrypt algorithm."""
def get_password_hash(password) -> str:
    return pwd_context.hash(password)

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