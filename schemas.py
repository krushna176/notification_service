from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from uuid import UUID

class UserCreate(BaseModel):
    email: Optional[EmailStr]
    phone: Optional[str]
    password: str

    pref_email: bool = False
    pref_sms: bool = False
    pref_push: bool = False
    pushover_user_key = str



class UserLogin(BaseModel):
    email: Optional[EmailStr]
    phone: Optional[str]
    password: str


class NotificationRequest(BaseModel):
    message: str
    priority: Literal["high", "medium", "low"] = "medium"

class NotificationCreate(BaseModel):
    message: str
    priority: Literal["high", "medium", "low"] = "medium"


class NotificationResponse(BaseModel):
    status: str


class PreferenceUpdate(BaseModel):
    pref_email: bool
    pref_sms: bool
    pref_push: bool