from celery import Celery, shared_task
import time


@shared_task
def test():
    print("hello")
    time.sleep(5)
    return "task completed"
