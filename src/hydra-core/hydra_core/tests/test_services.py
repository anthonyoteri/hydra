import pytest

from hydra_core import models, services


@pytest.mark.django_db
def test_update_settings():

    current_settings = models.Settings.objects.active()
    assert current_settings is not None

    assert current_settings.retention_period_days == 360
    assert current_settings.align_timestamps is False

    services.update_settings({"retention_period_days": 60})

    updated_settings = models.Settings.objects.active()

    assert updated_settings.retention_period_days == 60
    assert updated_settings.align_timestamps is False

    services.update_settings({"align_timestamps": True})
    updated_settings = models.Settings.objects.active()

    assert updated_settings.align_timestamps is True
    assert updated_settings.retention_period_days == 60
