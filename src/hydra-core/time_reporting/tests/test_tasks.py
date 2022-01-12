from datetime import timedelta

from django.conf import settings
from django.utils import timezone
import pytest

from hydra_core.models import Settings
from time_reporting.models import TimeRecord
from time_reporting.tasks import purge_old_records

from .factories import CategoryFactory, ProjectFactory, TimeRecordFactory


@pytest.mark.django_db
def test_purge_old_records():
    now = timezone.now()

    minimum = settings.MINIMUM_RETENTION_PERIOD_DAYS
    start = now - timedelta(days=minimum + 365)

    category = CategoryFactory()
    project = ProjectFactory(category=category)

    t = start
    while t < now:
        TimeRecordFactory.create(
            project=project, start_time=t, stop_time=t + timedelta(hours=8)
        )
        t = t + timedelta(days=1)

    # Make sure the total number of records matches the number of days
    assert TimeRecord.objects.count() == (
        (now - start).total_seconds() // timedelta(days=1).total_seconds()
    )

    # Make sure the oldest records started beyond the cutoff
    min_record = TimeRecord.objects.order_by("start_time").first()
    assert min_record.start_time == start

    # Configure the retention period to 180 days
    active_settings = Settings.objects.active()
    active_settings.retention_period_days = 180
    active_settings.save()

    purge_old_records()

    # Make sure the oldest record started < 180 days ago
    min_record = TimeRecord.objects.order_by("start_time").first()
    assert min_record.start_time == now - (timedelta(days=180))


@pytest.mark.django_db
def test_purge_old_records_below_minimum():
    now = timezone.now()

    minimum = settings.MINIMUM_RETENTION_PERIOD_DAYS
    start = now - timedelta(days=minimum + 365)

    category = CategoryFactory()
    project = ProjectFactory(category=category)

    t = start
    while t < now:
        TimeRecordFactory.create(
            project=project, start_time=t, stop_time=t + timedelta(hours=8)
        )
        t = t + timedelta(days=1)

    # Make sure the oldest records started beyond the cutoff
    min_record = TimeRecord.objects.order_by("start_time").first()
    assert min_record.start_time == start

    # Configure the retention period to below the minimum
    active_settings = Settings.objects.active()
    active_settings.retention_period_days = 1
    active_settings.save()

    purge_old_records()

    # Make sure we didn't delete more than the minimum
    min_record = TimeRecord.objects.order_by("start_time").first()
    assert min_record.start_time == now - (
        timedelta(days=settings.MINIMUM_RETENTION_PERIOD_DAYS)
    )


@pytest.mark.django_db
def test_purge_old_records_disabled():
    now = timezone.now()

    minimum = settings.MINIMUM_RETENTION_PERIOD_DAYS
    start = now - timedelta(days=minimum + 365)

    category = CategoryFactory()
    project = ProjectFactory(category=category)

    t = start
    while t < now:
        TimeRecordFactory.create(
            project=project, start_time=t, stop_time=t + timedelta(hours=8)
        )
        t = t + timedelta(days=1)

    # Make sure the oldest records started beyond the cutoff
    min_record = TimeRecord.objects.order_by("start_time").first()
    assert min_record.start_time == start

    # Configure the retention period to disable purging
    active_settings = Settings.objects.active()
    active_settings.retention_period_days = 0
    active_settings.save()

    purge_old_records()

    # Make sure we didn't delete anything
    min_record = TimeRecord.objects.order_by("start_time").first()
    assert min_record.start_time == start
