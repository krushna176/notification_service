from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas
from passlib.context import CryptContext
from auth import create_token

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)

    db_user = models.User(
        email=user.email,
        phone=user.phone,
        password=hashed_password,
        pref_email=user.pref_email,
        pref_sms=user.pref_sms,
        pref_push=user.pref_push
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User created"}

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        (models.User.email == user.email) |
        (models.User.phone == user.phone)
    ).first()

    if not db_user or not pwd_context.verify(user.password, db_user.password):
        return {"error": "Invalid credentials"}

    token = create_token({"user_id": str(db_user.id)})
    return {"access_token": token}