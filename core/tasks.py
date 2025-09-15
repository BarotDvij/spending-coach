from celery import shared_task

@shared_task
def ping(name="world"):
    return f"hello {name}"
