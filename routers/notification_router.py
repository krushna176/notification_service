from fastapi import Depends, APIRouter
from services.email_service import send_email
from services.sms_service import send_sms
from services.push_service import send_push
import schemas,models
from services.tasks import send_notification
from utils.get_current_user import get_current_user
from sqlalchemy.orm import Session
from uuid import UUID
from utils.logger import get_logger
logger = get_logger("api.notifications")

router = APIRouter()

from sqlalchemy.orm import Session
from database import SessionLocal

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/notifications", response_model=schemas.NotificationResponse)
def create_notification(
    req: schemas.NotificationCreate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"Notification request: {req}")
    logger.info(user.email)
    user_data = {
        "email": user.email,
        "phone": user.phone,
        "pushover_user_key": user.pushover_user_key,
        "pref_email": user.pref_email,
        "pref_sms": user.pref_sms,
        "pref_push": user.pref_push
    }
    send_notification.apply_async(
        args=[user_data, req.message],
        queue=req.priority
    )

    logger.info(f"Queued notification with priority {req.priority}")

    return {"status": f"{req.priority} notification queued"}

@router.get("/notifications/{id}")
def get_notification(id: UUID, db: Session = Depends(get_db)):
    notification = db.query(models.Notification).filter(
        models.Notification.id == id
    ).first()

    if not notification:
        return {"error": "Not found"}

    return {
        "id": notification.id,
        "status": notification.status,
        "message": notification.message
    }


@router.get("/users/me/notifications")
def get_my_notifications(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notifications = db.query(models.Notification).filter(
        models.Notification.user_id == user.id
    ).all()

    return notifications


@router.post("/users/me/preferences")
def update_my_preferences(
    prefs: schemas.PreferenceUpdate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user.pref_email = prefs.pref_email
    user.pref_sms = prefs.pref_sms
    user.pref_push = prefs.pref_push

    db.commit()

    return {"message": "Preferences updated"}


@router.get("/users/me/preferences")
def get_my_preferences(
    user: models.User = Depends(get_current_user)
):
    return {
        "pref_email": user.pref_email,
        "pref_sms": user.pref_sms,
        "pref_push": user.pref_push
    }