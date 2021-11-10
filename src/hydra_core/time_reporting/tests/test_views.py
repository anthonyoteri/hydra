from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
import pytest
from rest_framework import status

from time_reporting.models import Category, Project, SubProject, TimeRecord
from time_reporting.urls import app_name

from .factories import (
    CategoryFactory,
    ProjectFactory,
    SubProjectFactory,
    TimeRecordFactory,
)

CATEGORY_INDEX_VIEW = f"{app_name}:category_index"
CATEGORY_DETAIL_VIEW = f"{app_name}:category_detail"
PROJECT_INDEX_VIEW = f"{app_name}:project_index"
PROJECT_DETAIL_VIEW = f"{app_name}:project_detail"
SUB_PROJECT_INDEX_VIEW = f"{app_name}:subproject_index"
SUB_PROJECT_DETAIL_VIEW = f"{app_name}:subproject_detail"
TIME_RECORD_INDEX_VIEW = f"{app_name}:record_index"
TIME_RECORD_DETAIL_VIEW = f"{app_name}:record_detail"


@pytest.mark.django_db
def test_category_index_head(client):
    categories = CategoryFactory.create_batch(15)

    resp = client.head(reverse(CATEGORY_INDEX_VIEW))
    assert resp.status_code == status.HTTP_200_OK, resp.content
    assert resp.has_header("X-Result-Count")
    assert int(resp["X-Result-Count"]) == len(categories)


@pytest.mark.django_db
def test_category_index_get(client):
    categories = CategoryFactory.create_batch(5)

    resp = client.get(reverse(CATEGORY_INDEX_VIEW))
    assert resp.status_code == status.HTTP_200_OK, resp.content
    assert resp.has_header("X-Result-Count")
    assert int(resp["X-Result-Count"]) == len(categories)

    for got, expected in zip(resp.json(), categories):
        assert got["id"] == expected.id
        assert got["name"] == expected.name
        assert got["slug"] == expected.slug
        assert got["description"] == expected.description


@pytest.mark.django_db
def test_category_index_post(client):
    category_stub = CategoryFactory.stub()

    body = {
        "name": category_stub.name,
        "slug": category_stub.slug,
        "description": category_stub.description,
    }

    resp = client.post(reverse(CATEGORY_INDEX_VIEW), body, format="json")
    assert resp.status_code == status.HTTP_201_CREATED, resp.content

    assert resp.json()["name"] == category_stub.name
    assert resp.json()["slug"] == category_stub.slug
    assert resp.json()["description"] == category_stub.description

    assert resp.json()["id"] is not None
    assert resp.json()["created"] is not None
    assert resp.json()["updated"] is not None


@pytest.mark.django_db
def test_category_detail_get(client):
    category = CategoryFactory()

    resp = client.get(
        reverse(CATEGORY_DETAIL_VIEW, kwargs={"pk": category.pk})
    )
    assert resp.status_code == status.HTTP_200_OK, resp.contet

    assert resp.json()["name"] == category.name
    assert resp.json()["slug"] == category.slug
    assert resp.json()["description"] == category.description


@pytest.mark.django_db
def test_category_detail_delete(client):
    category = CategoryFactory()

    resp = client.delete(
        reverse(CATEGORY_DETAIL_VIEW, kwargs={"pk": category.pk})
    )
    assert resp.status_code == status.HTTP_204_NO_CONTENT, resp.content

    assert not Category.objects.filter(pk=category.pk).exists()


@pytest.mark.django_db
def test_category_detail_put(client):
    category = CategoryFactory()
    category_stub = CategoryFactory.stub()

    body = {
        "name": category_stub.name,
        "slug": category_stub.slug,
        "description": category_stub.description,
    }

    resp = client.put(
        reverse(CATEGORY_DETAIL_VIEW, kwargs={"pk": category.pk}),
        body,
        format="json",
    )
    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.json()["id"] == category.id
    assert resp.json()["name"] == category_stub.name
    assert resp.json()["slug"] == category_stub.slug
    assert resp.json()["description"] == category_stub.description


@pytest.mark.django_db
@pytest.mark.parametrize("field", ["name", "slug", "description"])
def test_category_detail_patch(field, client):

    category = CategoryFactory()
    category_stub = CategoryFactory.stub()

    body = {field: getattr(category_stub, field)}

    resp = client.patch(
        reverse(CATEGORY_DETAIL_VIEW, kwargs={"pk": category.pk}),
        body,
        format="json",
    )
    assert resp.status_code == status.HTTP_200_OK, resp.content

    for f in {"name", "slug", "description"} - {field}:
        assert resp.json()[f] == getattr(category, f)

    assert resp.json()[field] == getattr(category_stub, field)


@pytest.mark.django_db
def test_project_index_head(client):
    category = CategoryFactory()
    projects = ProjectFactory.create_batch(10, category=category)

    url = reverse(PROJECT_INDEX_VIEW, kwargs={"category_pk": category.pk})
    resp = client.head(url)

    assert resp.status_code == status.HTTP_200_OK, resp.content
    assert resp.has_header("X-Result-Count")
    assert int(resp["X-Result-Count"]) == len(projects)


@pytest.mark.django_db
def test_project_index_get(client):
    category = CategoryFactory()
    projects = ProjectFactory.create_batch(10, category=category)

    url = reverse(PROJECT_INDEX_VIEW, kwargs={"category_pk": category.pk})
    resp = client.get(url)

    assert resp.status_code == status.HTTP_200_OK, resp.content
    assert resp.has_header("X-Result-Count")
    assert int(resp["X-Result-Count"]) == len(projects)

    for got, expected in zip(resp.json(), projects):
        assert got["id"] == expected.id
        assert got["name"] == expected.name
        assert got["slug"] == expected.slug
        assert got["description"] == expected.description


@pytest.mark.django_db
def test_project_index_post(client):
    category = CategoryFactory()
    project_stub = ProjectFactory.stub(category=category)

    body = {
        "name": project_stub.name,
        "slug": project_stub.slug,
        "description": project_stub.description,
    }

    url = reverse(PROJECT_INDEX_VIEW, kwargs={"category_pk": category.pk})
    resp = client.post(url, body, format="json")

    assert resp.status_code == status.HTTP_201_CREATED, resp.content
    assert resp.json()["name"] == project_stub.name
    assert resp.json()["slug"] == project_stub.slug
    assert resp.json()["description"] == project_stub.description

    assert resp.json()["id"] is not None
    assert resp.json()["created"] is not None
    assert resp.json()["updated"] is not None


@pytest.mark.django_db
def test_project_detail_get(client):
    category = CategoryFactory()
    project = ProjectFactory(category=category)

    url = reverse(
        PROJECT_DETAIL_VIEW,
        kwargs={"category_pk": category.pk, "pk": project.pk},
    )
    resp = client.get(url)

    assert resp.status_code == status.HTTP_200_OK, resp.contet
    assert resp.json()["name"] == project.name
    assert resp.json()["slug"] == project.slug
    assert resp.json()["description"] == project.description


@pytest.mark.django_db
def test_project_detail_delete(client):
    category = CategoryFactory()
    project = ProjectFactory(category=category)

    url = reverse(
        PROJECT_DETAIL_VIEW,
        kwargs={"category_pk": category.pk, "pk": project.pk},
    )
    resp = client.delete(url)

    assert resp.status_code == status.HTTP_204_NO_CONTENT, resp.content

    assert not Project.objects.filter(pk=project.pk).exists()


@pytest.mark.django_db
def test_project_detail_put(client):
    category = CategoryFactory()
    project = ProjectFactory(category=category)
    project_stub = ProjectFactory.stub(category=category)

    body = {
        "name": project_stub.name,
        "slug": project_stub.slug,
        "description": project_stub.description,
    }
    url = reverse(
        PROJECT_DETAIL_VIEW,
        kwargs={"category_pk": category.pk, "pk": project.pk},
    )
    resp = client.put(url, body, format="json")

    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.json()["id"] == project.id
    assert resp.json()["name"] == project_stub.name
    assert resp.json()["slug"] == project_stub.slug
    assert resp.json()["description"] == project_stub.description


@pytest.mark.django_db
@pytest.mark.parametrize("field", ["name", "slug", "description"])
def test_project_detail_patch(field, client):

    category = CategoryFactory()
    project = ProjectFactory(category=category)
    project_stub = ProjectFactory.stub(category=category)

    body = {field: getattr(project_stub, field)}

    url = reverse(
        PROJECT_DETAIL_VIEW,
        kwargs={"category_pk": category.pk, "pk": project.pk},
    )
    resp = client.patch(url, body, format="json")

    assert resp.status_code == status.HTTP_200_OK, resp.content

    for f in {"name", "slug", "description"} - {field}:
        assert resp.json()[f] == getattr(project, f)

    assert resp.json()[field] == getattr(project_stub, field)


@pytest.mark.django_db
def test_project_detail_put_category(client):

    category_1 = CategoryFactory()
    category_2 = CategoryFactory()

    project = ProjectFactory(category=category_1)

    body = {
        "category": category_2.pk,
        "name": project.name,
        "slug": project.slug,
        "description": project.description,
    }

    url_1 = reverse(
        PROJECT_DETAIL_VIEW,
        kwargs={"category_pk": category_1.pk, "pk": project.pk},
    )
    url_2 = reverse(
        PROJECT_DETAIL_VIEW,
        kwargs={"category_pk": category_2.pk, "pk": project.pk},
    )

    resp = client.put(url_1, body, format="json")
    assert resp.status_code == status.HTTP_200_OK, resp.content

    resp_2 = client.get(url_2)
    assert resp_2.status_code == status.HTTP_200_OK, resp.content

    assert resp_2.json()["id"] == project.id
    assert resp_2.json()["name"] == project.name
    assert resp_2.json()["slug"] == project.slug
    assert resp_2.json()["description"] == project.description

    resp_3 = client.get(url_1)
    assert resp_3.status_code == status.HTTP_404_NOT_FOUND, resp.content


@pytest.mark.django_db
def test_project_detail_patch_category(client):

    category_1 = CategoryFactory()
    category_2 = CategoryFactory()

    project = ProjectFactory(category=category_1)

    body = {
        "category": category_2.pk,
    }

    url_1 = reverse(
        PROJECT_DETAIL_VIEW,
        kwargs={"category_pk": category_1.pk, "pk": project.pk},
    )
    url_2 = reverse(
        PROJECT_DETAIL_VIEW,
        kwargs={"category_pk": category_2.pk, "pk": project.pk},
    )

    resp = client.patch(url_1, body, format="json")
    assert resp.status_code == status.HTTP_200_OK, resp.content

    resp_2 = client.get(url_2)
    assert resp_2.status_code == status.HTTP_200_OK, resp.content

    assert resp_2.json()["id"] == project.id
    assert resp_2.json()["name"] == project.name
    assert resp_2.json()["slug"] == project.slug
    assert resp_2.json()["description"] == project.description

    resp_3 = client.get(url_1)
    assert resp_3.status_code == status.HTTP_404_NOT_FOUND, resp.content


@pytest.mark.django_db
def test_sub_project_index_head(client):
    category = CategoryFactory()
    project = ProjectFactory(category=category)
    sub_projects = SubProjectFactory.create_batch(5, project=project)

    url = reverse(
        SUB_PROJECT_INDEX_VIEW,
        kwargs={"project_pk": project.pk},
    )
    resp = client.head(url)

    assert resp.status_code == status.HTTP_200_OK, resp.content
    assert resp.has_header("X-Result-Count")
    assert int(resp["X-Result-Count"]) == len(sub_projects)


@pytest.mark.django_db
def test_sub_project_index_get(client):
    category = CategoryFactory()
    project = ProjectFactory(category=category)
    sub_projects = SubProjectFactory.create_batch(10, project=project)

    url = reverse(
        SUB_PROJECT_INDEX_VIEW,
        kwargs={"project_pk": project.pk},
    )
    resp = client.get(url)

    assert resp.status_code == status.HTTP_200_OK, resp.content
    assert resp.has_header("X-Result-Count")
    assert int(resp["X-Result-Count"]) == len(sub_projects)

    for got, expected in zip(resp.json(), sub_projects):
        assert got["id"] == expected.id
        assert got["name"] == expected.name
        assert got["slug"] == expected.slug
        assert got["description"] == expected.description


@pytest.mark.django_db
def test_sub_project_index_post(client):
    category = CategoryFactory()
    project = ProjectFactory(category=category)
    sub_project_stub = SubProjectFactory.stub(project=project)

    body = {
        "name": sub_project_stub.name,
        "slug": sub_project_stub.slug,
        "description": sub_project_stub.description,
    }

    url = reverse(
        SUB_PROJECT_INDEX_VIEW,
        kwargs={"project_pk": project.pk},
    )
    resp = client.post(url, body, format="json")

    assert resp.status_code == status.HTTP_201_CREATED, resp.content
    assert resp.json()["name"] == sub_project_stub.name
    assert resp.json()["slug"] == sub_project_stub.slug
    assert resp.json()["description"] == sub_project_stub.description

    assert resp.json()["id"] is not None
    assert resp.json()["created"] is not None
    assert resp.json()["updated"] is not None


@pytest.mark.django_db
def test_sub_project_detail_get(client):
    category = CategoryFactory()
    project = ProjectFactory(category=category)
    sub_project = SubProjectFactory(project=project)

    url = reverse(
        SUB_PROJECT_DETAIL_VIEW,
        kwargs={
            "project_pk": project.pk,
            "pk": sub_project.pk,
        },
    )
    resp = client.get(url)

    assert resp.status_code == status.HTTP_200_OK, resp.contet
    assert resp.json()["name"] == sub_project.name
    assert resp.json()["slug"] == sub_project.slug
    assert resp.json()["description"] == sub_project.description


@pytest.mark.django_db
def test_sub_project_detail_delete(client):
    category = CategoryFactory()
    project = ProjectFactory(category=category)
    sub_project = SubProjectFactory(project=project)

    url = reverse(
        SUB_PROJECT_DETAIL_VIEW,
        kwargs={
            "project_pk": project.pk,
            "pk": sub_project.pk,
        },
    )
    resp = client.delete(url)

    assert resp.status_code == status.HTTP_204_NO_CONTENT, resp.content

    assert not SubProject.objects.filter(pk=sub_project.pk).exists()


@pytest.mark.django_db
def test_sub_project_detail_put(client):
    category = CategoryFactory()
    project = ProjectFactory(category=category)
    sub_project = SubProjectFactory(project=project)
    sub_project_stub = SubProjectFactory.stub(project=project)

    body = {
        "name": sub_project_stub.name,
        "slug": sub_project_stub.slug,
        "description": sub_project_stub.description,
    }
    url = reverse(
        SUB_PROJECT_DETAIL_VIEW,
        kwargs={
            "project_pk": project.pk,
            "pk": sub_project.pk,
        },
    )
    resp = client.put(url, body, format="json")

    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.json()["id"] == sub_project.id
    assert resp.json()["name"] == sub_project_stub.name
    assert resp.json()["slug"] == sub_project_stub.slug
    assert resp.json()["description"] == sub_project_stub.description


@pytest.mark.django_db
@pytest.mark.parametrize("field", ["name", "slug", "description"])
def test_sub_project_detail_patch(field, client):

    category = CategoryFactory()
    project = ProjectFactory(category=category)
    sub_project = SubProjectFactory(project=project)
    sub_project_stub = SubProjectFactory.stub(project=project)

    body = {field: getattr(sub_project_stub, field)}

    url = reverse(
        SUB_PROJECT_DETAIL_VIEW,
        kwargs={
            "project_pk": project.pk,
            "pk": sub_project.pk,
        },
    )
    resp = client.patch(url, body, format="json")

    assert resp.status_code == status.HTTP_200_OK, resp.content

    for f in {"name", "slug", "description"} - {field}:
        assert resp.json()[f] == getattr(sub_project, f)

    assert resp.json()[field] == getattr(sub_project_stub, field)


@pytest.mark.django_db
def test_sub_project_detail_put_project(client):

    category = CategoryFactory()

    project_1 = ProjectFactory(category=category)
    project_2 = ProjectFactory(category=category)

    sub_project = SubProjectFactory(project=project_1)

    body = {
        "project": project_2.pk,
        "name": sub_project.name,
        "slug": sub_project.slug,
        "description": sub_project.description,
    }

    url_1 = reverse(
        SUB_PROJECT_DETAIL_VIEW,
        kwargs={
            "project_pk": project_1.pk,
            "pk": sub_project.pk,
        },
    )
    url_2 = reverse(
        SUB_PROJECT_DETAIL_VIEW,
        kwargs={
            "project_pk": project_2.pk,
            "pk": sub_project.pk,
        },
    )

    resp = client.put(url_1, body, format="json")
    assert resp.status_code == status.HTTP_200_OK, resp.content

    resp_2 = client.get(url_2)
    assert resp_2.status_code == status.HTTP_200_OK, resp.content

    assert resp_2.json()["id"] == sub_project.id
    assert resp_2.json()["name"] == sub_project.name
    assert resp_2.json()["slug"] == sub_project.slug
    assert resp_2.json()["description"] == sub_project.description

    resp_3 = client.get(url_1)
    assert resp_3.status_code == status.HTTP_404_NOT_FOUND, resp.content


@pytest.mark.django_db
def test_sub_project_detail_patch_project(client):

    category = CategoryFactory()

    project_1 = ProjectFactory(category=category)
    project_2 = ProjectFactory(category=category)

    sub_project = SubProjectFactory(project=project_1)

    body = {
        "project": project_2.pk,
    }

    url_1 = reverse(
        SUB_PROJECT_DETAIL_VIEW,
        kwargs={
            "project_pk": project_1.pk,
            "pk": sub_project.pk,
        },
    )
    url_2 = reverse(
        SUB_PROJECT_DETAIL_VIEW,
        kwargs={
            "project_pk": project_2.pk,
            "pk": sub_project.pk,
        },
    )

    resp = client.patch(url_1, body, format="json")
    assert resp.status_code == status.HTTP_200_OK, resp.content

    resp_2 = client.get(url_2)
    assert resp_2.status_code == status.HTTP_200_OK, resp.content

    assert resp_2.json()["id"] == sub_project.id
    assert resp_2.json()["name"] == sub_project.name
    assert resp_2.json()["slug"] == sub_project.slug
    assert resp_2.json()["description"] == sub_project.description

    resp_3 = client.get(url_1)
    assert resp_3.status_code == status.HTTP_404_NOT_FOUND, resp.content


@pytest.mark.django_db
def test_records_index_get(client):
    sub_project = SubProjectFactory()
    now = timezone.now()

    record_1 = TimeRecordFactory(
        sub_project=sub_project,
        start_time=now - timedelta(hours=8),
        total_seconds=timedelta(hours=3).total_seconds(),
    )
    record_2 = TimeRecordFactory(
        sub_project=sub_project,
        start_time=now - timedelta(hours=5),
        total_seconds=timedelta(hours=3).total_seconds(),
    )
    record_3 = TimeRecordFactory(
        sub_project=sub_project,
        start_time=now - timedelta(hours=2),
        total_seconds=0,
    )

    resp = client.get(reverse(TIME_RECORD_INDEX_VIEW))
    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.has_header("X-Result-Count")
    assert int(resp["X-Result-Count"]) == 3

    result_1, result_2, result_3 = resp.json()

    assert result_1["sub_project"] == sub_project.slug
    assert (
        result_1["start_time"]
        == timezone.localtime(record_1.start_time).isoformat()
    )
    assert (
        result_1["stop_time"]
        == timezone.localtime(record_1.stop_time).isoformat()
    )
    assert result_1["total_seconds"] == record_1.total_seconds

    assert result_2["sub_project"] == sub_project.slug
    assert (
        result_2["start_time"]
        == timezone.localtime(record_2.start_time).isoformat()
    )
    assert (
        result_2["stop_time"]
        == timezone.localtime(record_2.stop_time).isoformat()
    )
    assert result_2["total_seconds"] == record_2.total_seconds

    assert result_3["sub_project"] == sub_project.slug
    assert (
        result_3["start_time"]
        == timezone.localtime(record_3.start_time).isoformat()
    )
    assert (
        result_3["stop_time"]
        == timezone.localtime(record_3.stop_time).isoformat()
    )
    assert result_3["total_seconds"] == record_3.total_seconds


@pytest.mark.django_db
def test_records_index_get_preserves_order(client):
    sub_project = SubProjectFactory()
    now = timezone.now()

    TimeRecordFactory(
        sub_project=sub_project,
        start_time=now - timedelta(hours=8),
        total_seconds=timedelta(hours=3).total_seconds(),
    )
    TimeRecordFactory(
        sub_project=sub_project,
        start_time=now - timedelta(hours=2),
        total_seconds=0,
    )
    TimeRecordFactory(
        sub_project=sub_project,
        start_time=now - timedelta(hours=5),
        total_seconds=timedelta(hours=3).total_seconds(),
    )

    resp = client.get(reverse(TIME_RECORD_INDEX_VIEW))
    assert resp.status_code == status.HTTP_200_OK, resp.content

    timestamps = [r["start_time"] for r in resp.json()]

    timestamps_sorted = sorted(timestamps)
    assert timestamps == timestamps_sorted


@pytest.mark.django_db
def test_records_index_post(client):

    sub_project = SubProjectFactory()
    now = timezone.now()

    body = {
        "sub_project": sub_project.slug,
        "start_time": now.isoformat(),
    }

    resp = client.post(reverse(TIME_RECORD_INDEX_VIEW), body, format="json")
    assert resp.status_code == status.HTTP_201_CREATED, resp.content

    assert resp.json() == {
        "id": 1,
        "sub_project": sub_project.slug,
        "start_time": timezone.localtime(now).isoformat(),
        "stop_time": timezone.localtime(now).isoformat(),
        "total_seconds": 0,
    }


@pytest.mark.django_db
def test_records_detail_get(client):

    now = timezone.now()
    record = TimeRecordFactory(start_time=now)

    url = reverse(TIME_RECORD_DETAIL_VIEW, kwargs={"pk": record.pk})
    resp = client.get(url)

    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.json() == {
        "id": 1,
        "sub_project": record.sub_project.slug,
        "start_time": timezone.localtime(record.start_time).isoformat(),
        "stop_time": timezone.localtime(record.stop_time).isoformat(),
        "total_seconds": record.total_seconds,
    }


@pytest.mark.django_db
def test_records_detail_delete(client):

    record = TimeRecordFactory()

    url = reverse(TIME_RECORD_DETAIL_VIEW, kwargs={"pk": record.pk})
    resp = client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT, resp.content

    assert not TimeRecord.objects.filter(pk=record.pk).exists()


@pytest.mark.django_db
def test_records_detail_put(client):

    record = TimeRecordFactory()
    record_stub = TimeRecordFactory.stub(total_seconds=3600)

    body = {
        "sub_project": record.sub_project.slug,
        "start_time": timezone.localtime(record_stub.start_time).isoformat(),
        "stop_time": timezone.localtime(
            record_stub.start_time
            + timedelta(seconds=record_stub.total_seconds)
        ).isoformat(),
    }

    url = reverse(TIME_RECORD_DETAIL_VIEW, kwargs={"pk": record.pk})
    resp = client.put(url, body, format="json")

    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.json() == {
        "id": record.id,
        "sub_project": record.sub_project.slug,
        "start_time": body["start_time"],
        "stop_time": body["stop_time"],
        "total_seconds": record_stub.total_seconds,
    }


@pytest.mark.django_db
def test_records_detail_patch_field_sub_project(client):

    sub_project_1 = SubProjectFactory()
    sub_project_2 = SubProjectFactory()

    record = TimeRecordFactory(sub_project=sub_project_1)
    record_stub = TimeRecordFactory.stub(sub_project=sub_project_2)

    body = {"sub_project": record_stub.sub_project.slug}

    url = reverse(TIME_RECORD_DETAIL_VIEW, kwargs={"pk": record.pk})
    resp = client.patch(url, body, format="json")

    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.json()["sub_project"] == record_stub.sub_project.slug


@pytest.mark.django_db
def test_records_detail_patch_field_start_time(client):
    record = TimeRecordFactory()
    record_stub = TimeRecordFactory.stub()

    body = {
        "start_time": timezone.localtime(record_stub.start_time).isoformat()
    }

    url = reverse(TIME_RECORD_DETAIL_VIEW, kwargs={"pk": record.pk})
    resp = client.patch(url, body, format="json")

    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.json()["start_time"] == body["start_time"]


@pytest.mark.django_db
def test_records_detail_patch_field_stop_time(client):
    record = TimeRecordFactory()
    record_stub = TimeRecordFactory.stub(total_seconds=3600)

    body = {
        "stop_time": timezone.localtime(
            record_stub.start_time
            + timedelta(seconds=record_stub.total_seconds)
        ).isoformat()
    }

    url = reverse(TIME_RECORD_DETAIL_VIEW, kwargs={"pk": record.pk})
    resp = client.patch(url, body, format="json")

    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.json()["stop_time"] == body["stop_time"]
