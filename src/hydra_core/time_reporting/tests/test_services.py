from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
import pytest

from hydra_core.auth import delete_user
from time_reporting import models, services

from .factories import CategoryFactory, ProjectFactory, TimeRecordFactory


@pytest.mark.django_db
def test_create_category(user):

    category_stub = CategoryFactory.stub()

    category = services.create_category(
        user=user,
        name=category_stub.name,
        description=category_stub.description,
    )

    assert category.name == category_stub.name
    assert category.description == category_stub.description


@pytest.mark.django_db
def test_update_category(user):
    category = CategoryFactory(user=user)
    category_stub = CategoryFactory.stub()

    persisted = services.update_category(
        pk=category.pk,
        user=user,
        name=category_stub.name,
        description=category_stub.description,
    )

    assert persisted.created == category.created
    assert persisted.updated > category.updated
    assert persisted.pk == category.id

    assert persisted.name == category_stub.name
    assert persisted.description == category_stub.description


@pytest.mark.django_db
@pytest.mark.parametrize("field", ["name", "description"])
def test_partial_update_category(field, user):
    category = CategoryFactory(user=user)
    category_stub = CategoryFactory.stub()

    kwargs = {field: getattr(category_stub, field)}

    persisted = services.patch_category(
        pk=category.pk,
        user=user,
        **kwargs,
    )

    for attr in {"name", "description"} - {field}:
        assert getattr(persisted, attr) == getattr(
            category, attr
        ), f"Mismatch of field {attr}"

    assert getattr(persisted, field) == getattr(
        category_stub, field
    ), f"Mismatch of field {field}"

    assert persisted.created == category.created
    assert persisted.updated > category.updated
    assert persisted.pk == category.pk


@pytest.mark.django_db
def test_delete_category(user):
    category = CategoryFactory(user=user)
    services.delete_category(pk=category.pk)
    assert not models.Category.objects.filter(pk=category.pk).exists()


@pytest.mark.django_db
def test_delete_category_cascades(user):

    category = CategoryFactory(user=user)

    project_1 = ProjectFactory(category=category)
    project_2 = ProjectFactory(category=category)

    services.delete_category(pk=category.pk)

    assert not models.Category.objects.filter(pk=category.pk).exists()
    assert not models.Project.objects.filter(pk=project_1.pk).exists()
    assert not models.Project.objects.filter(pk=project_2.pk).exists()


@pytest.mark.django_db
def test_delete_category_with_records_not_allowed(user):
    category = CategoryFactory(user=user)

    project = ProjectFactory(category=category)

    TimeRecordFactory(project=project)

    # The existence of a record should prevent deletion
    with pytest.raises(IntegrityError):
        services.delete_category(pk=category.pk)


@pytest.mark.django_db
def test_create_project(user):
    category = CategoryFactory(user=user)
    project_stub = ProjectFactory.stub(category=category)

    project = services.create_project(
        category=project_stub.category,
        name=project_stub.name,
        description=project_stub.description,
    )

    assert project.category == category
    assert project.name == project_stub.name
    assert project.description == project_stub.description


@pytest.mark.django_db
def test_update_project(user):
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)
    new_category = CategoryFactory(user=user)
    project_stub = ProjectFactory.stub(category=new_category)

    persisted = services.update_project(
        pk=project.pk,
        category=project_stub.category,
        name=project_stub.name,
        description=project_stub.description,
    )

    assert persisted.created == project.created
    assert persisted.updated > project.updated
    assert persisted.pk == project.id

    assert persisted.category == project_stub.category
    assert persisted.name == project_stub.name
    assert persisted.description == project_stub.description


@pytest.mark.django_db
@pytest.mark.parametrize("field", ["category", "name", "description"])
def test_partial_update_project(field, user):
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)
    new_category = CategoryFactory(user=user)
    project_stub = ProjectFactory.stub(category=new_category)

    kwargs = {field: getattr(project_stub, field)}

    persisted = services.patch_project(
        pk=project.pk,
        **kwargs,
    )

    for attr in {"category", "name", "description"} - {field}:
        assert getattr(persisted, attr) == getattr(
            project, attr
        ), f"Mismatch of field {attr}"

    assert getattr(persisted, field) == getattr(
        project_stub, field
    ), f"Mismatch of field {field}"

    assert persisted.created == project.created
    assert persisted.updated > project.updated
    assert persisted.pk == project.pk


@pytest.mark.django_db
def test_delete_project(user):
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)
    services.delete_project(pk=project.pk)
    assert not models.Project.objects.filter(pk=project.pk).exists()


@pytest.mark.django_db
def test_delete_project_with_records_not_allowed(user):
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)

    TimeRecordFactory(project=project)

    # The existence of a record should prevent deletion
    with pytest.raises(IntegrityError):
        services.delete_project(pk=project.pk)


@pytest.mark.django_db
@pytest.mark.parametrize("with_stop_time", [False, True])
def test_create_record(with_stop_time, user):
    now = timezone.now()
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)
    start_time = now - timedelta(hours=1)
    stop_time = now

    if with_stop_time:
        record = services.create_record(
            project=project,
            start_time=start_time,
            stop_time=stop_time,
        )
    else:
        record = services.create_record(
            project=project,
            start_time=start_time,
        )

    assert record.project == project
    assert record.start_time == start_time

    if with_stop_time:
        assert record.stop_time == stop_time
        assert record.total_seconds == int(
            (stop_time - start_time).total_seconds()
        )
    else:
        assert record.stop_time is None
        assert record.total_seconds is None


@pytest.mark.django_db
def test_create_record_fails_negative_duration(user):
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)

    start_time = timezone.now().replace(microsecond=0)
    stop_time = start_time - timedelta(hours=1)

    with pytest.raises(ValidationError):
        services.create_record(
            project=project,
            start_time=start_time,
            stop_time=stop_time,
        )


@pytest.mark.django_db
def test_update_record(user):
    now = timezone.now()
    category = CategoryFactory(user=user)

    project = ProjectFactory(category=category)
    new_project = ProjectFactory(category=category)

    record = TimeRecordFactory(
        project=project,
        start_time=now - timedelta(hours=5),
        stop_time=now - timedelta(hours=1),
    )
    record_stub = TimeRecordFactory.stub(
        project=new_project,
        start_time=record.start_time - timedelta(hours=1),
        stop_time=record.stop_time - timedelta(hours=1),  # type: ignore
    )

    persisted = services.update_record(
        pk=record.pk,
        project=new_project,
        start_time=record_stub.start_time,
        stop_time=record_stub.stop_time,
    )

    assert persisted.pk == record.pk
    assert persisted.project == new_project
    assert persisted.start_time == record_stub.start_time
    assert persisted.stop_time == record_stub.stop_time


@pytest.mark.django_db
@pytest.mark.parametrize("field", ["project", "start_time", "stop_time"])
def test_partial_update_record(field, user):
    now = timezone.now()
    category = CategoryFactory(user=user)
    project_1 = ProjectFactory(category=category)
    project_2 = ProjectFactory(category=category)

    record = TimeRecordFactory(
        project=project_1, start_time=now - timedelta(hours=2), stop_time=now
    )

    if field == "project":
        persisted = services.patch_record(pk=record.pk, project=project_2)
        assert persisted.project == project_2

    elif field == "start_time":
        t = record.start_time - timedelta(hours=1)
        persisted = services.patch_record(pk=record.pk, start_time=t)
        assert persisted.start_time == t

    else:
        t = record.stop_time - timedelta(hours=1)  # type: ignore
        persisted = services.patch_record(pk=record.pk, stop_time=t)
        assert persisted.stop_time == t


@pytest.mark.django_db
def test_delete_record(user):
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)
    record = TimeRecordFactory(project=project)
    services.delete_record(pk=record.pk)
    assert not models.TimeRecord.objects.filter(pk=record.pk).exists()


# TODO: The following test case doesn't really belong to services, but
# there really isn't a better place to test this functionality since it
# is heavily dependent on verifying that the models are cleaned up after
# removing a user.
@pytest.mark.django_db
def test_delete_user_cascades(user):

    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)
    record = TimeRecordFactory(project=project)

    delete_user(username=user.username)

    assert not models.Category.objects.filter(pk=category.pk).exists()
    assert not models.Project.objects.filter(pk=project.pk).exists()
    assert not models.TimeRecord.objects.filter(pk=record.pk).exists()
