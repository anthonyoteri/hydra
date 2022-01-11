from datetime import timedelta
from itertools import chain
import random

from django.urls import reverse
from django.utils import timezone
import pytest
from rest_framework import status

from time_reporting.models import Category, Project, TimeRecord
from time_reporting.urls import app_name

from .factories import CategoryFactory, ProjectFactory, TimeRecordFactory

CATEGORY_INDEX_VIEW = f"{app_name}:category_index"
CATEGORY_DETAIL_VIEW = f"{app_name}:category_detail"
CONFIG_VIEW = f"{app_name}:config"
PROJECT_INDEX_VIEW = f"{app_name}:project_index"
PROJECT_DETAIL_VIEW = f"{app_name}:project_detail"
TIME_RECORD_INDEX_VIEW = f"{app_name}:record_index"
TIME_RECORD_DETAIL_VIEW = f"{app_name}:record_detail"


@pytest.mark.django_db
def test_category_index_head(client, user):
    categories = CategoryFactory.create_batch(15, user=user)

    resp = client.head(reverse(CATEGORY_INDEX_VIEW))
    assert resp.status_code == status.HTTP_200_OK, resp.content
    assert resp.has_header("X-Result-Count")
    assert int(resp["X-Result-Count"]) == len(categories)


@pytest.mark.django_db
def test_category_index_get(client, user):
    categories = CategoryFactory.create_batch(5, user=user)

    resp = client.get(reverse(CATEGORY_INDEX_VIEW))
    assert resp.status_code == status.HTTP_200_OK, resp.content
    assert resp.has_header("X-Result-Count")
    assert int(resp["X-Result-Count"]) == len(categories)

    for got, expected in zip(resp.json(), categories):
        assert got["id"] == expected.id
        assert got["name"] == expected.name
        assert got["description"] == expected.description


@pytest.mark.django_db
def test_category_index_post(client):
    category_stub = CategoryFactory.stub()

    body = {
        "name": category_stub.name,
        "description": category_stub.description,
    }

    resp = client.post(reverse(CATEGORY_INDEX_VIEW), body, format="json")
    assert resp.status_code == status.HTTP_201_CREATED, resp.content

    assert resp.json()["name"] == category_stub.name
    assert resp.json()["description"] == category_stub.description

    assert resp.json()["id"] is not None
    assert resp.json()["created"] is not None
    assert resp.json()["updated"] is not None


@pytest.mark.django_db
def test_category_detail_get(client, user):
    category = CategoryFactory(user=user)

    resp = client.get(
        reverse(CATEGORY_DETAIL_VIEW, kwargs={"pk": category.pk})
    )
    assert resp.status_code == status.HTTP_200_OK, resp.contet

    assert resp.json()["name"] == category.name
    assert resp.json()["description"] == category.description


@pytest.mark.django_db
def test_category_detail_delete(client, user):
    category = CategoryFactory(user=user)

    resp = client.delete(
        reverse(CATEGORY_DETAIL_VIEW, kwargs={"pk": category.pk})
    )
    assert resp.status_code == status.HTTP_204_NO_CONTENT, resp.content

    assert not Category.objects.filter(pk=category.pk).exists()


@pytest.mark.django_db
def test_category_detail_put(client, user):
    category = CategoryFactory(user=user)
    category_stub = CategoryFactory.stub()

    body = {
        "name": category_stub.name,
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
    assert resp.json()["description"] == category_stub.description


@pytest.mark.django_db
@pytest.mark.parametrize("field", ["name", "description"])
def test_category_detail_patch(field, client, user):

    category = CategoryFactory(user=user)
    category_stub = CategoryFactory.stub()

    body = {field: getattr(category_stub, field)}

    resp = client.patch(
        reverse(CATEGORY_DETAIL_VIEW, kwargs={"pk": category.pk}),
        body,
        format="json",
    )
    assert resp.status_code == status.HTTP_200_OK, resp.content

    for f in {"name", "description"} - {field}:
        assert resp.json()[f] == getattr(category, f)

    assert resp.json()[field] == getattr(category_stub, field)


@pytest.mark.django_db
def test_project_index_head(client, user):
    category = CategoryFactory(user=user)
    projects = ProjectFactory.create_batch(10, category=category)

    url = reverse(PROJECT_INDEX_VIEW)
    resp = client.head(url)

    assert resp.status_code == status.HTTP_200_OK, resp.content
    assert resp.has_header("X-Result-Count")
    assert int(resp["X-Result-Count"]) == len(projects)


@pytest.mark.django_db
def test_project_index_get(client, user):
    category = CategoryFactory(user=user)
    projects = ProjectFactory.create_batch(10, category=category)

    url = reverse(PROJECT_INDEX_VIEW)
    resp = client.get(url)

    assert resp.status_code == status.HTTP_200_OK, resp.content
    assert resp.has_header("X-Result-Count")
    assert int(resp["X-Result-Count"]) == len(projects)

    for got, expected in zip(resp.json(), projects):
        assert got["id"] == expected.id
        assert got["name"] == expected.name
        assert got["description"] == expected.description
        assert got["category"] == expected.category.pk
        assert got["created"] is not None
        assert got["updated"] is not None


@pytest.mark.django_db
def test_project_index_post(client, user):
    category = CategoryFactory(user=user)
    project_stub = ProjectFactory.stub(category=category)

    body = {
        "name": project_stub.name,
        "category": category.pk,
        "description": project_stub.description,
    }

    url = reverse(PROJECT_INDEX_VIEW)
    resp = client.post(url, body, format="json")

    assert resp.status_code == status.HTTP_201_CREATED, resp.content
    assert resp.json()["id"] > 0
    assert resp.json()["name"] == project_stub.name
    assert resp.json()["description"] == project_stub.description
    assert resp.json()["category"] == category.pk
    assert resp.json()["created"] is not None
    assert resp.json()["updated"] is not None


@pytest.mark.django_db
def test_project_detail_get(client, user):
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)

    url = reverse(
        PROJECT_DETAIL_VIEW,
        kwargs={"pk": project.pk},
    )
    resp = client.get(url)

    assert resp.status_code == status.HTTP_200_OK, resp.contet
    assert resp.json()["id"] > 0
    assert resp.json()["name"] == project.name
    assert resp.json()["description"] == project.description
    assert resp.json()["category"] == project.category.pk
    assert resp.json()["created"] is not None
    assert resp.json()["updated"] is not None


@pytest.mark.django_db
def test_project_detail_delete(client, user):
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)

    url = reverse(
        PROJECT_DETAIL_VIEW,
        kwargs={"pk": project.pk},
    )
    resp = client.delete(url)

    assert resp.status_code == status.HTTP_204_NO_CONTENT, resp.content

    assert not Project.objects.filter(pk=project.pk).exists()


@pytest.mark.django_db
def test_project_detail_put(client, user):
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)
    project_stub = ProjectFactory.stub(category=category)

    body = {
        "name": project_stub.name,
        "description": project_stub.description,
        "category": category.pk,
    }
    url = reverse(
        PROJECT_DETAIL_VIEW,
        kwargs={"pk": project.pk},
    )
    resp = client.put(url, body, format="json")

    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.json()["id"] == project.id
    assert resp.json()["name"] == project_stub.name
    assert resp.json()["category"] == category.pk
    assert resp.json()["description"] == project_stub.description
    assert resp.json()["created"] is not None
    assert resp.json()["updated"] is not None


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field",
    [
        "name",
        "description",
    ],
)
def test_project_detail_patch(field, client, user):

    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)
    project_stub = ProjectFactory.stub(category=category)

    body = {field: getattr(project_stub, field)}

    url = reverse(
        PROJECT_DETAIL_VIEW,
        kwargs={"pk": project.pk},
    )
    resp = client.patch(url, body, format="json")

    assert resp.status_code == status.HTTP_200_OK, resp.content

    for f in {"name", "description"} - {field}:
        assert resp.json()[f] == getattr(project, f)

    assert resp.json()[field] == getattr(project_stub, field)


@pytest.mark.django_db
def test_project_detail_patch_category(client, user):

    category_1 = CategoryFactory(user=user)
    category_2 = CategoryFactory(user=user)

    project = ProjectFactory(category=category_1)

    body = {
        "category": category_2.pk,
    }

    url = reverse(
        PROJECT_DETAIL_VIEW,
        kwargs={"pk": project.pk},
    )

    resp = client.patch(url, body, format="json")
    assert resp.status_code == status.HTTP_200_OK, resp.content

    resp_2 = client.get(url)
    assert resp_2.status_code == status.HTTP_200_OK, resp.content

    assert resp_2.json()["id"] == project.id
    assert resp_2.json()["name"] == project.name
    assert resp_2.json()["description"] == project.description
    assert resp_2.json()["category"] == category_2.pk
    assert resp_2.json()["created"] is not None
    assert resp_2.json()["updated"] is not None


@pytest.mark.django_db
def test_records_index_get(client, user):
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)
    now = timezone.now()

    record_1 = TimeRecordFactory(
        project=project,
        start_time=now - timedelta(hours=8),
        stop_time=now - timedelta(hours=5),
    )
    record_2 = TimeRecordFactory(
        project=project,
        start_time=now - timedelta(hours=5),
        stop_time=now - timedelta(hours=2),
    )
    record_3 = TimeRecordFactory(
        project=project,
        start_time=now - timedelta(hours=2),
    )

    resp = client.get(reverse(TIME_RECORD_INDEX_VIEW))
    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.has_header("X-Result-Count")
    assert int(resp["X-Result-Count"]) == 3

    result_1, result_2, result_3 = resp.json()

    assert result_1["project"] == project.pk
    assert (
        result_1["start_time"]
        == timezone.localtime(record_1.start_time).isoformat()
    )
    assert (
        result_1["stop_time"]
        == timezone.localtime(record_1.stop_time).isoformat()
    )
    assert result_1["approved"] == record_1.approved

    assert result_2["project"] == project.pk
    assert (
        result_2["start_time"]
        == timezone.localtime(record_2.start_time).isoformat()
    )
    assert (
        result_2["stop_time"]
        == timezone.localtime(record_2.stop_time).isoformat()
    )
    assert result_2["approved"] == record_2.approved

    assert result_3["project"] == project.pk
    assert (
        result_3["start_time"]
        == timezone.localtime(record_3.start_time).isoformat()
    )
    assert result_3["stop_time"] is None
    assert result_3["approved"] == record_3.approved


@pytest.mark.django_db
def test_records_index_get_preserves_order(client, user):
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)
    now = timezone.now()

    TimeRecordFactory(
        project=project,
        start_time=now - timedelta(hours=8),
        stop_time=now - timedelta(hours=5),
    )
    TimeRecordFactory(
        project=project,
        start_time=now - timedelta(hours=2),
    )
    TimeRecordFactory(
        project=project,
        start_time=now - timedelta(hours=5),
        stop_time=now - timedelta(hours=2),
    )

    resp = client.get(reverse(TIME_RECORD_INDEX_VIEW))
    assert resp.status_code == status.HTTP_200_OK, resp.content

    timestamps = [r["start_time"] for r in resp.json()]

    timestamps_sorted = sorted(timestamps)
    assert timestamps == timestamps_sorted


@pytest.mark.django_db
def test_records_index_post(client, user):
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)

    now = timezone.now()

    body = {
        "project": project.pk,
        "start_time": (now - timedelta(hours=2)).isoformat(),
        "stop_time": (now - timedelta(hours=1)).isoformat(),
        "approved": True,
    }

    resp = client.post(reverse(TIME_RECORD_INDEX_VIEW), body, format="json")
    assert resp.status_code == status.HTTP_201_CREATED, resp.content

    record = TimeRecord.objects.filter(project=project.pk).last()
    assert resp.json() == {
        "id": record.pk,
        "project": project.pk,
        "start_time": timezone.localtime(now - timedelta(hours=2)).isoformat(),
        "stop_time": timezone.localtime(now - timedelta(hours=1)).isoformat(),
        "total_seconds": 3600,
        "approved": True,
    }


@pytest.mark.django_db
def test_records_index_post_no_stop_time(client, user):
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)

    now = timezone.now()

    body = {
        "project": project.pk,
        "start_time": (now - timedelta(hours=2)).isoformat(),
        "approved": True,
    }

    resp = client.post(reverse(TIME_RECORD_INDEX_VIEW), body, format="json")
    assert resp.status_code == status.HTTP_201_CREATED, resp.content

    record = TimeRecord.objects.filter(project=project.pk).last()
    assert resp.json() == {
        "id": record.pk,
        "project": project.pk,
        "start_time": timezone.localtime(now - timedelta(hours=2)).isoformat(),
        "stop_time": None,
        "total_seconds": None,
        "approved": True,
    }


@pytest.mark.django_db
@pytest.mark.parametrize("future", [False, True])
def test_records_index_post_no_approved(future, client, user):
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)

    now = timezone.now()

    if future:
        start_time = now + timedelta(hours=2)
    else:
        start_time = now - timedelta(hours=2)
    stop_time = start_time + timedelta(hours=1)

    body = {
        "project": project.pk,
        "start_time": start_time.isoformat(),
        "stop_time": stop_time.isoformat(),
    }

    resp = client.post(reverse(TIME_RECORD_INDEX_VIEW), body, format="json")
    assert resp.status_code == status.HTTP_201_CREATED, resp.content

    record = TimeRecord.objects.filter(project=project.pk).last()
    assert resp.json() == {
        "id": record.pk,
        "project": project.pk,
        "start_time": timezone.localtime(start_time).isoformat(),
        "stop_time": timezone.localtime(stop_time).isoformat(),
        "total_seconds": 3600,
        "approved": not future,
    }


@pytest.mark.django_db
def test_records_detail_get(client, user):
    now = timezone.now()
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)

    now = timezone.now()
    record = TimeRecordFactory(
        project=project, start_time=now - timedelta(hours=3), stop_time=now
    )

    url = reverse(TIME_RECORD_DETAIL_VIEW, kwargs={"pk": record.pk})
    resp = client.get(url)

    assert resp.status_code == status.HTTP_200_OK, resp.content

    record = TimeRecord.objects.filter(project=project.pk).last()
    assert resp.json() == {
        "id": record.pk,
        "project": record.project.pk,
        "start_time": timezone.localtime(record.start_time).isoformat(),
        "stop_time": timezone.localtime(record.stop_time).isoformat(),
        "total_seconds": record.total_seconds,
        "approved": record.approved,
    }


@pytest.mark.django_db
def test_records_detail_delete(client, user):
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)
    record = TimeRecordFactory(project=project)

    url = reverse(TIME_RECORD_DETAIL_VIEW, kwargs={"pk": record.pk})
    resp = client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT, resp.content

    assert not TimeRecord.objects.filter(pk=record.pk).exists()


@pytest.mark.django_db
def test_records_detail_put(client, user):
    now = timezone.now()
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)
    record = TimeRecordFactory(
        project=project,
        start_time=now - timedelta(hours=5),
        stop_time=now - timedelta(hours=1),
    )
    record_stub = TimeRecordFactory.stub(
        project=project,
        start_time=record.start_time + timedelta(hours=1),
        stop_time=record.stop_time + timedelta(hours=1),  # type: ignore
        approved=not record.approved,
    )

    body = {
        "project": record.project.pk,
        "start_time": timezone.localtime(record_stub.start_time).isoformat(),
        "stop_time": timezone.localtime(record_stub.stop_time).isoformat(),
        "approved": record_stub.approved,
    }

    url = reverse(TIME_RECORD_DETAIL_VIEW, kwargs={"pk": record.pk})
    resp = client.put(url, body, format="json")

    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.json() == {
        "id": record.id,
        "project": record.project.pk,
        "start_time": body["start_time"],
        "stop_time": body["stop_time"],
        "total_seconds": int(timedelta(hours=4).total_seconds()),
        "approved": body["approved"],
    }


@pytest.mark.django_db
def test_records_detail_patch_field_project(client, user):
    category = CategoryFactory(user=user)

    project_1 = ProjectFactory(category=category)
    project_2 = ProjectFactory(category=category)

    record = TimeRecordFactory(project=project_1)
    record_stub = TimeRecordFactory.stub(project=project_2)

    body = {"project": record_stub.project.pk}

    url = reverse(TIME_RECORD_DETAIL_VIEW, kwargs={"pk": record.pk})
    resp = client.patch(url, body, format="json")

    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.json()["project"] == record_stub.project.pk


@pytest.mark.django_db
def test_records_detail_patch_field_start_time(client, user):
    now = timezone.now()
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)
    record = TimeRecordFactory(
        project=project, start_time=now - timedelta(hours=2), stop_time=now
    )
    record_stub = TimeRecordFactory.stub(
        project=project,
        start_time=record.start_time + timedelta(hours=1),
        stop_time=record.stop_time,
    )

    body = {
        "start_time": timezone.localtime(record_stub.start_time).isoformat()
    }

    url = reverse(TIME_RECORD_DETAIL_VIEW, kwargs={"pk": record.pk})
    resp = client.patch(url, body, format="json")

    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.json()["start_time"] == body["start_time"]


@pytest.mark.parametrize("null_stop_time", [False, True])
@pytest.mark.django_db
def test_records_detail_patch_field_stop_time(null_stop_time, client, user):
    now = timezone.now()
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)
    record = TimeRecordFactory(
        project=project, start_time=now - timedelta(hours=2), stop_time=now
    )
    record_stub = TimeRecordFactory.stub(
        project=project,
        start_time=record.start_time,
        stop_time=record.stop_time - timedelta(hours=1),  # type: ignore
    )

    if not null_stop_time:
        body = {
            "stop_time": timezone.localtime(record_stub.stop_time).isoformat()
        }
    else:
        body = {"stop_time": None}

    url = reverse(TIME_RECORD_DETAIL_VIEW, kwargs={"pk": record.pk})
    resp = client.patch(url, body, format="json")

    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.json()["stop_time"] == body["stop_time"]


@pytest.mark.django_db
def test_records_detail_patch_field_approved(client, user):
    category = CategoryFactory(user=user)
    project = ProjectFactory(category=category)
    record = TimeRecordFactory(
        project=project,
    )

    body = {"approved": not record.approved}

    url = reverse(TIME_RECORD_DETAIL_VIEW, kwargs={"pk": record.pk})
    resp = client.patch(url, body, format="json")

    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.json()["approved"] == body["approved"]


@pytest.mark.django_db
def test_config_get(client, user):

    category1 = CategoryFactory(user=user)
    category2 = CategoryFactory(user=user)

    ProjectFactory.create_batch(2, category=category1)
    ProjectFactory.create_batch(2, category=category2)

    all_projects = Project.objects.filter(
        category__in=(category1, category2)
    ).all()
    TimeRecordFactory.create_batch(16, project=random.choice(all_projects))

    url = reverse(CONFIG_VIEW)

    resp = client.get(url)
    assert resp.status_code == status.HTTP_200_OK, resp.content

    body = resp.json()

    assert len(body["categories"]) == 2
    assert len(body["projects"]) == 4
    assert len(body["time_records"]) == 16


@pytest.mark.django_db
def test_config_put(client, user):

    category1 = CategoryFactory(user=user)
    category2 = CategoryFactory(user=user)
    project1 = ProjectFactory(category=category1)
    project2 = ProjectFactory(category=category2)
    record1 = TimeRecordFactory(project=project1)
    record2 = TimeRecordFactory(project=project2)

    data = {
        "categories": [
            {
                "id": c.id,
                "user": c.user.username,
                "name": c.name,
                "description": c.description,
            }
            for c in (category1, category2)
        ],
        "projects": [
            {
                "id": p.id,
                "category": p.category.id,
                "name": p.name,
                "description": p.description,
            }
            for p in (project1, project2)
        ],
        "time_records": [
            {
                "id": t.id,
                "project": t.project.id,
                "start_time": t.start_time.isoformat(),
                "stop_time": (
                    t.stop_time.isoformat()  # type: ignore
                    if t.stop_time is not None
                    else None
                ),
            }
            for t in (record1, record2)
        ],
    }

    # Make sure we delete all records so that we can validate the results
    TimeRecord.objects.all().delete()
    Project.objects.all().delete()
    Category.objects.all().delete()

    resp = client.put(reverse(CONFIG_VIEW), data, format="json")
    assert resp.status_code == status.HTTP_200_OK, resp.content

    for category in data["categories"]:
        got = Category.objects.get(pk=category["id"])
        assert got.user.username == category["user"]
        assert got.name == category["name"]
        assert got.description == category["description"]

    for project in data["projects"]:
        got = Project.objects.get(pk=project["id"])
        assert got.category.id == project["category"]
        assert got.name == project["name"]
        assert got.description == project["description"]

    for record in data["time_records"]:
        got = TimeRecord.objects.get(pk=record["id"])
        assert got.project.id == record["project"]
        assert got.start_time.isoformat() == record["start_time"]
        if record["stop_time"] is None:
            assert got.stop_time is None
        else:
            assert got.stop_time.isoformat() == record["stop_time"]


@pytest.mark.django_db
def test_config_get_put_together(client, user):
    categories = CategoryFactory.create_batch(10, user=user)
    projects = list(
        chain(
            *map(
                lambda c: ProjectFactory.create_batch(3, category=c),
                categories,
            )
        )
    )
    records = list(
        chain(
            *map(
                lambda p: TimeRecordFactory.create_batch(10, project=p),
                projects,
            )
        )
    )

    resp = client.get(reverse(CONFIG_VIEW))
    assert resp.status_code == status.HTTP_200_OK, resp.content

    body = resp.json()
    resp = client.put(reverse(CONFIG_VIEW), body, format="json")
    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert Category.objects.count() == len(categories)
    assert Project.objects.count() == len(projects)
    assert TimeRecord.objects.count() == len(records)

    for got, expected in zip(
        Category.objects.all().order_by("id"),
        sorted(categories, key=lambda c: c.id),
    ):
        assert got.id == expected.id
        assert got.user == expected.user
        assert got.name == expected.name
        assert got.description == expected.description

    for got, expected in zip(
        Project.objects.all().order_by("id"),
        sorted(projects, key=lambda p: p.id),
    ):
        assert got.id == expected.id
        assert got.category == expected.category
        assert got.name == expected.name
        assert got.description == expected.description

    for got, expected in zip(
        TimeRecord.objects.all().order_by("id"),
        sorted(records, key=lambda r: r.id),
    ):
        assert got.id == expected.id
        assert got.project == expected.project
        assert got.start_time == expected.start_time
        assert got.stop_time == expected.stop_time
