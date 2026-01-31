# src/api/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt

from ..schemas.user import UserCreate, UserRead, UserLogin
from ...models import database
from ...services import user_service
from ...config import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

# -------------------- TOKEN --------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.BETTER_AUTH_SECRET,
        algorithm=ALGORITHM
    )

# -------------------- DB --------------------
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- SIGNUP --------------------
@router.post("/signup", response_model=UserRead)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if user_service.get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )

    if user_service.get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    db_user = user_service.create_user(db, user)
    return db_user

# -------------------- LOGIN (EMAIL) --------------------
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = user_service.get_user_by_email(db, data.email)

    if not user or not user_service.verify_password(
        data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        },
        "token": access_token
    }
