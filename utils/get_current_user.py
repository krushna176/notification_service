from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from uuid import UUID
from database import SessionLocal
import models
from decouple import config

security = HTTPBearer()
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = UUID(payload["user_id"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    db = SessionLocal()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    db.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user