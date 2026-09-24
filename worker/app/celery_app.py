import os

from celery import Celery

celery_app = Celery(
    "dhcp_manager",
    broker=os.getenv("DHCP_MANAGER_REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("DHCP_MANAGER_REDIS_URL", "redis://redis:6379/0"),
)
celery_app.conf.update(task_serializer="json", result_serializer="json", accept_content=["json"])
