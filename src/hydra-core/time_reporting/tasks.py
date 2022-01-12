from datetime import datetime, timedelta
import time

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from hydra_core.models import Settings

from .models import TimeRecord

log = get_task_logger(__name__)


@shared_task
@transaction.atomic
def purge_old_records():

    active_settings = Settings.objects.active()
    if active_settings.retention_period_days == 0:
        log.debug("Purging old records has been disabled")
        return

    if (
        active_settings.retention_period_days
        <= settings.MINIMUM_RETENTION_PERIOD_DAYS
    ):
        log.warning(
            "Configured retention period %d is below the minimum",
            active_settings.retention_period_days,
        )
        active_settings.retention_period_days = (
            settings.MINIMUM_RETENTION_PERIOD_DAYS
        )

    now = (
        time.time() // 86400 * 86400
    )  # Floor the date to the start of the current day UTC
    cutoff = timezone.make_aware(
        datetime.fromtimestamp(
            now
            - timedelta(
                days=active_settings.retention_period_days
            ).total_seconds()
        )
    )
    log.info("Purging all records started before %s", cutoff.isoformat())

    TimeRecord.objects.filter(start_time__lte=cutoff).delete()
