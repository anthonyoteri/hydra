from datetime import timedelta
import os

from celery import Celery

__all__ = ("app",)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hydra_core.settings")

app = Celery("hydra_core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "purge_old_records": {
        "task": "time_reporting.tasks.purge_old_records",
        "schedule": timedelta(days=1),
        "options": {
            "expires": timedelta(days=1).total_seconds(),
        },
    },
}
