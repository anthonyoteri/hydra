from datetime import timedelta

from django.db import models
from django.utils import timezone


class Category(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    description = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Project(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    description = models.TextField(null=True, blank=True)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="projects"
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class SubProject(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    description = models.TextField(null=True, blank=True)

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="sub_projects"
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class TimeRecord(models.Model):

    sub_project = models.ForeignKey(
        SubProject, on_delete=models.PROTECT, related_name="records"
    )
    start_time = models.DateTimeField(default=timezone.now)
    total_seconds = models.PositiveIntegerField(default=0)

    @property
    def stop_time(self):
        return timezone.localtime(self.start_time) + timedelta(
            seconds=self.total_seconds
        )
