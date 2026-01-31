# from sqlalchemy.orm import Session
# from ..models.user import User
# from ..api.schemas.user import UserCreate
# from typing import Optional

# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# def get_user_by_username(db: Session, username: str) -> Optional[User]:
#     return db.query(User).filter(User.username == username).first()

# def get_user_by_email(db: Session, email: str) -> Optional[User]:
#     return db.query(User).filter(User.email == email).first()

# def create_user(db: Session, user: UserCreate) -> User:
#     hashed_password = get_password_hash(user.password)
#     db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user






# src/services/user_service.py
from sqlalchemy.orm import Session
from typing import Optional
from passlib.context import CryptContext

from ..models.user import User
from ..api.schemas.user import UserCreate  # ✅ cleaner import

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------- PASSWORD --------------------
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# -------------------- QUERIES --------------------
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

# -------------------- CREATE USER --------------------
def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
