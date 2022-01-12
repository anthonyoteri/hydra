import logging

from django.db import transaction

from .models import Settings

log = logging.getLogger(__name__)


@transaction.atomic
def update_settings(settings: dict):

    if not settings:
        return

    active_settings = Settings.objects.active()
    active_settings.pk = None
    active_settings.id = None

    dirty = False
    protected_fields = {"id", "pk", "created"}
    for attr, value in settings.items():

        if attr in protected_fields:
            continue

        if getattr(active_settings, attr) != value:
            dirty = True
        setattr(active_settings, attr, value)

    if not dirty:
        return

    active_settings.save()
    log.info("settings updated: %s", active_settings)
