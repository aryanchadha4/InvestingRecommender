# backend/app/services/tasks/task_utils.py

from celery import Task
from time import sleep


class RetriableTask(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 3, "countdown": 5}
    retry_backoff = True
    retry_jitter = True


def respectful_sleep(seconds: float):
    # use for 429 backoff if your provider rate-limits
    try:
        sleep(seconds)
    except Exception:
        pass

