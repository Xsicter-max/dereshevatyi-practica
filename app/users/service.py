from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash

from app.users.models import User
from app.users.schemas import UserRegisterRequest


password_hash = PasswordHash.recommended()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def register_user(db: Session, data: UserRegisterRequest) -> User:
    existing = get_user_by_username(db, data.username)
    if existing is not None:
        raise ValueError("username_taken")

    user = User(
        username=data.username,
        password_hash=password_hash.hash(data.password),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("username_taken")
    db.refresh(user)
    return user