from __future__ import annotations

from datetime import datetime

from django.db import transaction
from django.utils.text import slugify

from .models import Category, Project, TimeRecord


@transaction.atomic
def create_category(
    *,
    pk: int | None = None,
    name: str,
    description: str | None = None,
):
    category = Category(pk=pk, name=name, description=description)
    category.save()

    return category


@transaction.atomic
def update_category(
    *,
    pk: int | None = None,
    name: str,
    description: str | None = None,
):

    category = Category.objects.get(pk=pk)

    category.name = name
    category.description = description

    category.save()
    return category


@transaction.atomic
def patch_category(
    *,
    pk: int | None = None,
    **kwargs,
):
    category = Category.objects.get(pk=pk)

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
    slug: str | None = None,
    description: str | None = None,
):

    if slug is None:
        slug = slugify(name)

    project = category.projects.create(
        pk=pk, name=name, slug=slug, description=description
    )
    project.save()

    return project


@transaction.atomic
def update_project(
    *,
    pk: int | None = None,
    category: Category,
    name: str,
    slug: str | None = None,
    description: str | None = None,
):

    project = Project.objects.get(pk=pk)

    project.category = category
    project.name = name
    project.slug = slug
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
    project.slug = kwargs.get("slug", project.slug)
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
    total_seconds: int = 0,
):

    last = (
        TimeRecord.objects.filter(total_seconds=0)
        .order_by("start_time")
        .last()
    )
    if last:
        last.total_seconds = (start_time - last.start_time).total_seconds()
        last.save()

    if stop_time is not None:
        total_seconds = int((stop_time - start_time).total_seconds())

    record = project.records.create(
        pk=pk,
        start_time=start_time,
        total_seconds=total_seconds,
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
    total_seconds: int = 0,
):

    record = TimeRecord.objects.get(pk=pk)

    record.project = project
    record.start_time = start_time.replace(microsecond=0)

    if stop_time is not None:
        record.total_seconds = int(
            (stop_time - record.start_time).total_seconds()
        )
    else:
        record.total_seconds = total_seconds

    record.save()

    return record


@transaction.atomic
def patch_record(*, pk: int | None = None, **kwargs):

    record = TimeRecord.objects.get(pk=pk)

    record.project = kwargs.get("project", record.project)
    record.start_time = kwargs.get("start_time", record.start_time).replace(
        microsecond=0
    )

    if "stop_time" in kwargs:
        record.total_seconds = (
            kwargs["stop_time"] - record.start_time
        ).total_seconds()
    else:
        record.total_seconds = kwargs.get(
            "total_seconds", record.total_seconds
        )

    record.save()

    return record


@transaction.atomic
def delete_record(*, pk: int | None = None):
    TimeRecord.objects.filter(pk=pk).delete()
