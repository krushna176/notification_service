from celery import Celery

celery = Celery(
    "notification_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.task_routes = {
    "tasks.send_notification": {"queue": "default"}
}
celery.autodiscover_tasks(["services"])