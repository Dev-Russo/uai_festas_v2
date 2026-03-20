from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.models.user import User
from backend.schemas.user import PasswordChange
from backend.utils.security import verify_password, get_password_hash
from fastapi import HTTPException

def update_user_password(db: Session, user: User, data_password: PasswordChange) -> User:
    
    if not verify_password(data_password.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Senha Atual Errada")
    
    user.hashed_password = get_password_hash(data_password.new_password)

    db.commit()
    db.refresh(user)

    return user
    