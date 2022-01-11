from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Category(models.Model):
    class Meta:
        unique_together = ("user", "name")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="projects"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TimeRecord(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.PROTECT, related_name="records"
    )
    start_time = models.DateTimeField(default=timezone.now)
    stop_time = models.DateTimeField(default=None, null=True, blank=True)

    approved = models.BooleanField(default=False)

    def clean(self):
        if self.stop_time is not None:
            if self.stop_time < self.start_time:
                raise ValidationError("Stop time must be after start time")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def total_seconds(self):
        if self.stop_time is not None:
            return int((self.stop_time - self.start_time).total_seconds())
        return None

    def __str__(self):
        return f"{self.start_time.isoformat()} - {self.project.name}"
