# backend/app/services/tasks/celery_app.py

from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app = Celery(
    "invest",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        "app.services.tasks.price_tasks",
        "app.services.tasks.signal_tasks",
        "app.services.tasks.orchestrate",
        "app.services.tasks.schedule",
    ],
)

app.conf.update(
    task_acks_late=True,
    worker_prefetch_multiplier=1,  # better fairness on long tasks
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

