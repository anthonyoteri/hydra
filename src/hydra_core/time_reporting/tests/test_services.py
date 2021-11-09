from datetime import timedelta

from django.db.utils import IntegrityError
from django.utils import timezone
from django.utils.text import slugify
import pytest

from time_reporting import models, services

from .factories import (
    CategoryFactory,
    ProjectFactory,
    SubProjectFactory,
    TimeRecordFactory,
)


@pytest.mark.django_db
def test_create_category():

    category_stub = CategoryFactory.stub()

    category = services.create_category(
        name=category_stub.name,
        slug=category_stub.slug,
        description=category_stub.description,
    )

    assert category.name == category_stub.name
    assert category.slug == category_stub.slug
    assert category.description == category_stub.description


@pytest.mark.django_db
def test_create_category_blank_slug():
    category_stub = CategoryFactory.stub(name="Foo Bar Baz")

    category = services.create_category(name=category_stub.name)

    assert category.name == category_stub.name
    assert category.slug == slugify(category_stub.name)


@pytest.mark.django_db
def test_update_category():
    category = CategoryFactory()
    category_stub = CategoryFactory.stub()

    persisted = services.update_category(
        pk=category.pk,
        name=category_stub.name,
        slug=category_stub.slug,
        description=category_stub.description,
    )

    assert persisted.created == category.created
    assert persisted.updated > category.updated
    assert persisted.pk == category.id

    assert persisted.name == category_stub.name
    assert persisted.slug == category_stub.slug
    assert persisted.description == category_stub.description


@pytest.mark.django_db
@pytest.mark.parametrize("field", ["name", "slug", "description"])
def test_partial_update_category(field):
    category = CategoryFactory()
    category_stub = CategoryFactory.stub()

    kwargs = {field: getattr(category_stub, field)}

    persisted = services.patch_category(
        pk=category.pk,
        **kwargs,
    )

    for attr in {"name", "slug", "description"} - {field}:
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
def test_delete_category():
    category = CategoryFactory()
    services.delete_category(pk=category.pk)
    assert not models.Category.objects.filter(pk=category.pk).exists()


@pytest.mark.django_db
def test_delete_category_cascades():

    category = CategoryFactory()

    project_1 = ProjectFactory(category=category)
    project_2 = ProjectFactory(category=category)

    sub_project_1 = SubProjectFactory(project=project_1)
    sub_project_2 = SubProjectFactory(project=project_2)

    services.delete_category(pk=category.pk)

    assert not models.Category.objects.filter(pk=category.pk).exists()
    assert not models.Project.objects.filter(pk=project_1.pk).exists()
    assert not models.Project.objects.filter(pk=project_2.pk).exists()
    assert not models.SubProject.objects.filter(pk=sub_project_1.pk).exists()
    assert not models.SubProject.objects.filter(pk=sub_project_2.pk).exists()


@pytest.mark.django_db
def test_delete_category_with_records_not_allowed():
    category = CategoryFactory()

    project = ProjectFactory(category=category)
    sub_project = SubProjectFactory(project=project)

    TimeRecordFactory(sub_project=sub_project)

    # The existence of a record should prevent deletion
    with pytest.raises(IntegrityError):
        services.delete_category(pk=category.pk)


@pytest.mark.django_db
def test_create_project():
    category = CategoryFactory()
    project_stub = ProjectFactory.stub(category=category)

    project = services.create_project(
        category=project_stub.category,
        name=project_stub.name,
        slug=project_stub.slug,
        description=project_stub.description,
    )

    assert project.category == category
    assert project.name == project_stub.name
    assert project.slug == project_stub.slug
    assert project.description == project_stub.description


@pytest.mark.django_db
def test_update_project():
    project = ProjectFactory()
    new_category = CategoryFactory()
    project_stub = ProjectFactory.stub(category=new_category)

    persisted = services.update_project(
        pk=project.pk,
        category=project_stub.category,
        name=project_stub.name,
        slug=project_stub.slug,
        description=project_stub.description,
    )

    assert persisted.created == project.created
    assert persisted.updated > project.updated
    assert persisted.pk == project.id

    assert persisted.category == project_stub.category
    assert persisted.name == project_stub.name
    assert persisted.slug == project_stub.slug
    assert persisted.description == project_stub.description


@pytest.mark.django_db
@pytest.mark.parametrize("field", ["category", "name", "slug", "description"])
def test_partial_update_project(field):
    project = ProjectFactory()
    new_category = CategoryFactory()
    project_stub = ProjectFactory.stub(category=new_category)

    kwargs = {field: getattr(project_stub, field)}

    persisted = services.patch_project(
        pk=project.pk,
        **kwargs,
    )

    for attr in {"category", "name", "slug", "description"} - {field}:
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
def test_delete_project():
    project = ProjectFactory()
    services.delete_project(pk=project.pk)
    assert not models.Project.objects.filter(pk=project.pk).exists()


@pytest.mark.django_db
def test_delete_project_cascades():
    project = ProjectFactory()
    sub_project = SubProjectFactory(project=project)

    services.delete_project(pk=project.pk)

    assert not models.Project.objects.filter(pk=project.pk).exists()
    assert not models.SubProject.objects.filter(pk=sub_project.pk).exists()


@pytest.mark.django_db
def test_delete_project_with_records_not_allowed():
    project = ProjectFactory()
    sub_project = SubProjectFactory(project=project)

    TimeRecordFactory(sub_project=sub_project)

    # The existence of a record should prevent deletion
    with pytest.raises(IntegrityError):
        services.delete_project(pk=project.pk)


@pytest.mark.django_db
def test_create_sub_project():
    category = CategoryFactory()
    project = ProjectFactory(category=category)
    sub_project_stub = SubProjectFactory.stub(project=project)

    sub_project = services.create_sub_project(
        project=sub_project_stub.project,
        name=sub_project_stub.name,
        slug=sub_project_stub.slug,
        description=sub_project_stub.description,
    )

    assert sub_project.project == project
    assert sub_project.name == sub_project_stub.name
    assert sub_project.slug == sub_project_stub.slug
    assert sub_project.description == sub_project_stub.description


@pytest.mark.django_db
def test_update_sub_project():
    sub_project = SubProjectFactory()
    new_project = ProjectFactory()
    sub_project_stub = SubProjectFactory.stub(project=new_project)

    persisted = services.update_sub_project(
        pk=sub_project.pk,
        project=sub_project_stub.project,
        name=sub_project_stub.name,
        slug=sub_project_stub.slug,
        description=sub_project_stub.description,
    )

    assert persisted.created == sub_project.created
    assert persisted.updated > sub_project.updated
    assert persisted.pk == sub_project.id

    assert persisted.name == sub_project_stub.name
    assert persisted.slug == sub_project_stub.slug
    assert persisted.description == sub_project_stub.description


@pytest.mark.django_db
@pytest.mark.parametrize("field", ["project", "name", "slug", "description"])
def test_partial_update_sub_project(field):
    sub_project = SubProjectFactory()
    new_project = ProjectFactory()
    sub_project_stub = SubProjectFactory.stub(project=new_project)

    kwargs = {field: getattr(sub_project_stub, field)}

    persisted = services.patch_sub_project(
        pk=sub_project.pk,
        **kwargs,
    )

    for attr in {"project", "name", "slug", "description"} - {field}:
        assert getattr(persisted, attr) == getattr(
            sub_project, attr
        ), f"Mismatch of field {attr}"

    assert getattr(persisted, field) == getattr(
        sub_project_stub, field
    ), f"Mismatch of field {field}"

    assert persisted.created == sub_project.created
    assert persisted.updated > sub_project.updated
    assert persisted.pk == sub_project.pk


@pytest.mark.django_db
def test_delete_sub_project():
    sub_project = SubProjectFactory()
    services.delete_sub_project(pk=sub_project.pk)
    assert not models.SubProject.objects.filter(pk=sub_project.pk).exists()


@pytest.mark.django_db
def test_delete_sub_project_with_records_not_allowed():
    sub_project = SubProjectFactory()

    TimeRecordFactory(sub_project=sub_project)

    # The existence of a record should prevent deletion
    with pytest.raises(IntegrityError):
        services.delete_sub_project(pk=sub_project.pk)


@pytest.mark.django_db
def test_create_record():
    sub_project = SubProjectFactory()

    start_time = timezone.now().replace(microsecond=0) - timedelta(hours=1)

    record = services.create_record(
        sub_project=sub_project,
        start_time=start_time,
        total_seconds=0,
    )

    assert record.sub_project == sub_project
    assert record.start_time == start_time
    assert record.total_seconds == 0


@pytest.mark.django_db
def test_create_record_positive_duration():
    sub_project = SubProjectFactory()

    start_time = timezone.now().replace(microsecond=0) - timedelta(hours=8)
    stop_time = start_time + timedelta(hours=4)

    record = services.create_record(
        sub_project=sub_project,
        start_time=start_time,
        total_seconds=(stop_time - start_time).total_seconds(),
    )

    assert record.sub_project == sub_project
    assert record.start_time == start_time
    assert record.total_seconds == (stop_time - start_time).total_seconds()
    assert record.stop_time == stop_time


@pytest.mark.django_db
def test_create_record_fails_negative_duration():
    sub_project = SubProjectFactory()

    start_time = timezone.now().replace(microsecond=0)
    stop_time = start_time - timedelta(hours=1)

    with pytest.raises(IntegrityError):
        services.create_record(
            sub_project=sub_project,
            start_time=start_time,
            total_seconds=(stop_time - start_time).total_seconds(),
        )


@pytest.mark.django_db
def test_create_record_finalizes_previous():
    sub_project = SubProjectFactory()

    start_time_1 = timezone.now().replace(microsecond=0) - timedelta(hours=8)

    record_1 = services.create_record(
        sub_project=sub_project, start_time=start_time_1, total_seconds=0
    )

    start_time_2 = start_time_1 + timedelta(hours=5)

    services.create_record(
        sub_project=sub_project, start_time=start_time_2, total_seconds=0
    )

    record_1 = models.TimeRecord.objects.get(pk=record_1.pk)

    assert record_1.total_seconds != 0
    assert record_1.stop_time == start_time_2


@pytest.mark.django_db
def test_update_record():
    sub_project = SubProjectFactory()
    new_sub_project = SubProjectFactory()
    new_start_time = timezone.now().replace(microsecond=0) - timedelta(hours=4)

    record = TimeRecordFactory(sub_project=sub_project)
    record_stub = TimeRecordFactory.stub(
        sub_project=new_sub_project, start_time=new_start_time
    )

    persisted = services.update_record(
        pk=record.pk,
        sub_project=new_sub_project,
        start_time=record_stub.start_time,
        total_seconds=record_stub.total_seconds,
    )

    assert persisted.pk == record.pk
    assert persisted.sub_project == new_sub_project
    assert persisted.start_time == record_stub.start_time
    assert persisted.total_seconds == record_stub.total_seconds


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field", ["sub_project", "start_time", "total_seconds"]
)
def test_partial_update_record(field):
    sub_project_1 = SubProjectFactory()
    sub_project_2 = SubProjectFactory()

    record = TimeRecordFactory(sub_project=sub_project_1)

    if field == "sub_project":
        persisted = services.patch_record(
            pk=record.pk, sub_project=sub_project_2
        )

        assert persisted.start_time == record.start_time
        assert persisted.stop_time == record.stop_time
        assert persisted.sub_project == sub_project_2
    elif field == "start_time":
        new_start_time = timezone.now().replace(microsecond=0) - timedelta(
            days=1
        )
        persisted = services.patch_record(
            pk=record.pk, start_time=new_start_time
        )
        assert persisted.start_time == new_start_time
        assert persisted.total_seconds == record.total_seconds
        assert persisted.sub_project == record.sub_project
    else:
        total_seconds = record.total_seconds + 1
        persisted = services.patch_record(
            pk=record.pk, total_seconds=total_seconds
        )
        assert persisted.start_time == record.start_time
        assert persisted.total_seconds == total_seconds
        assert persisted.sub_project == record.sub_project


@pytest.mark.django_db
def test_delete_record():
    record = TimeRecordFactory()
    services.delete_record(pk=record.pk)
    assert not models.TimeRecord.objects.filter(pk=record.pk).exists()
