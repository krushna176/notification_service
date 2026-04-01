from fastapi import FastAPI
from database import Base, engine
from routers import user_router, notification_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router.router, prefix="/user")
app.include_router(notification_router.router, prefix="/notification")
