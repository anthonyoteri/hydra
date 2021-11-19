from datetime import timedelta

from django.conf import settings
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
    total_seconds = models.PositiveIntegerField(default=0)

    @property
    def stop_time(self):
        return timezone.localtime(self.start_time) + timedelta(
            seconds=self.total_seconds
        )

    def __str__(self):
        return f"{self.start_time.isoformat()} - {self.project.name}"
