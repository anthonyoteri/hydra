from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class SettingsQuerySet(models.QuerySet):
    def active(self):
        return self.last()


class Settings(models.Model):
    objects = SettingsQuerySet.as_manager()

    retention_period_days = models.IntegerField(default=360)
    align_timestamps = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
