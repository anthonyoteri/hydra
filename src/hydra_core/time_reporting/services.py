from __future__ import annotations

from datetime import datetime
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction

from .models import Category, Project, TimeRecord

User = get_user_model()

log = logging.getLogger(__name__)


@transaction.atomic
def create_category(
    *,
    pk: int | None = None,
    user: settings.AUTH_USER_MODEL,
    name: str,
    description: str | None = None,
):
    category = Category(pk=pk, user=user, name=name, description=description)
    category.save()

    return category


@transaction.atomic
def update_category(
    *,
    pk: int | None = None,
    user: settings.AUTH_USER_MODEL,
    name: str,
    description: str | None = None,
):

    category = Category.objects.get(pk=pk)

    category.user = user
    category.name = name
    category.description = description

    category.save()
    return category


@transaction.atomic
def patch_category(
    *,
    pk: int | None = None,
    user: settings.AUTH_USER_MODEL,
    **kwargs,
):
    category = Category.objects.get(pk=pk)

    category.user = user
    category.name = kwargs.get("name", category.name)
    category.description = kwargs.get("description", category.description)

    category.save()
    return category


@transaction.atomic
def delete_category(*, pk: int | None = None):
    Category.objects.filter(pk=pk).delete()


@transaction.atomic
def create_project(
    *,
    pk: int | None = None,
    category: Category,
    name: str,
    description: str | None = None,
):
    project = category.projects.create(
        pk=pk,
        name=name,
        description=description,
    )
    project.save()

    return project


@transaction.atomic
def update_project(
    *,
    pk: int | None = None,
    category: Category,
    name: str,
    description: str | None = None,
):

    project = Project.objects.get(pk=pk)
    project.category = category
    project.name = name
    project.description = description

    project.save()
    return project


@transaction.atomic
def patch_project(
    *,
    pk: int | None = None,
    **kwargs,
):
    project = Project.objects.get(pk=pk)

    project.category = kwargs.get("category", project.category)
    project.name = kwargs.get("name", project.name)
    project.description = kwargs.get("description", project.description)

    project.save()
    return project


@transaction.atomic
def delete_project(*, pk: int | None = None):
    Project.objects.filter(pk=pk).delete()


@transaction.atomic
def create_record(
    *,
    pk: int | None = None,
    project: Project,
    start_time: datetime,
    stop_time: datetime | None = None,
):

    record = project.records.create(
        pk=pk,
        start_time=start_time,
        stop_time=stop_time,
    )
    record.save()
    return record


@transaction.atomic
def update_record(
    *,
    pk: int | None = None,
    project: Project,
    start_time: datetime,
    stop_time: datetime | None = None,
):

    record = TimeRecord.objects.get(pk=pk)
    record.project = project
    record.start_time = start_time
    record.stop_time = stop_time
    record.save()

    return record


@transaction.atomic
def patch_record(*, pk: int | None = None, **kwargs):
    record = TimeRecord.objects.get(pk=pk)

    record.project = kwargs.get("project", record.project)
    record.start_time = kwargs.get("start_time", record.start_time)
    record.stop_time = kwargs.get("stop_time", record.stop_time)
    record.save()

    return record


@transaction.atomic
def delete_record(*, pk: int | None = None):
    TimeRecord.objects.filter(pk=pk).delete()
