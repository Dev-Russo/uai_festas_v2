from passlib.context import CryptContext

"""Security utilities for password hashing and verification using bcrypt algorithm."""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""Functions for hashing and verifying passwords."""
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

"""Function to hash a password using bcrypt algorithm."""
def get_password_hash(password) -> str:
    return pwd_context.hash(password)