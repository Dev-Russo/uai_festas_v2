from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from dependencies import get_db
from models.user import User
from schemas.user import PasswordChange, UserCreate, UserUpdate, UserResponse
from utils.security import verify_password, get_password_hash, create_access_token
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

def register_user(db: Session, user: UserCreate) -> UserResponse:
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(name=user.name, email=user.email, role=user.role, is_active=user.is_active, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db: Session, user: OAuth2PasswordRequestForm) -> dict:
    from models.commissioner import Commissioner

    # Tenta login como usuário (admin/producer) pelo email
    db_user = db.query(User).filter(User.email == user.username).first()
    if db_user:
        if not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Email ou senha invalidos")
        access_token = create_access_token(
            data={"sub": db_user.email, "role": db_user.role, "user_type": "user"}
        )
        return {"access_token": access_token, "token_type": "bearer", "user_type": "user", "event_id": None}

    # Tenta login como comissário pelo username
    db_commissioner = db.query(Commissioner).filter(Commissioner.username == user.username).first()
    if db_commissioner:
        if not verify_password(user.password, db_commissioner.hashed_password):
            raise HTTPException(status_code=401, detail="Username ou senha invalidos")
        if not db_commissioner.is_active:
            raise HTTPException(status_code=401, detail="Conta de comissário inativa")
        access_token = create_access_token(
            data={
                "sub": db_commissioner.username,
                "role": db_commissioner.role,
                "user_type": "commissioner",
                "event_id": db_commissioner.event_id,
                "commissioner_group_id": db_commissioner.commissioner_group_id,
                "full_access": db_commissioner.full_access,
            }
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_type": "commissioner",
            "event_id": db_commissioner.event_id,
        }

    raise HTTPException(status_code=401, detail="Credenciais invalidas")

def get_user_profile(db: Session, current_user: User) -> UserResponse:
    return current_user

def update_user_profile(db: Session, current_user: User, user_data: UserUpdate) -> UserResponse:
    update_data = user_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")
    for key, value in update_data.items():
        setattr(current_user, key, value)
    try:
        db.commit()
        db.refresh(current_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="E-mail ou Nome de usuário já existe.")
    return current_user

def update_user_password(db: Session, user: User, data_password: PasswordChange) -> User:
    if not verify_password(data_password.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Senha Atual Errada")
    user.hashed_password = get_password_hash(data_password.new_password)
    db.commit()
    db.refresh(user)
    return user
    