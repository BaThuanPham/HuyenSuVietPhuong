from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.user import UserLogin,UserCreate
from models.user import User
from services.auth import verify_password
from services.token import create_access_token
from services.deps import get_db
from datetime import timedelta
from services.auth import hash_password, verify_password
from datetime import datetime, timedelta

router = APIRouter()


SECRET_KEY = "SECRET_KEY_HERE"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=user.email).first():
        raise HTTPException(status_code=400, detail="User already registered")
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    return {"msg": "User registered"}

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Thông tin đăng nhập không hợp lệ")
    # Tạo token không có hạn (hoặc có hạn rất dài)
    access_token = create_access_token(data={"sub": str(user.id)})

    # Lưu token mới vào DB
    user.current_token = access_token
    db.commit()
    return access_token