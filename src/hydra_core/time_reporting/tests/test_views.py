from django.urls import reverse
import pytest
from rest_framework import status

from time_reporting.models import Category, Project, SubProject
from time_reporting.urls import app_name

from .factories import CategoryFactory, ProjectFactory, SubProjectFactory

CATEGORY_INDEX_VIEW = f"{app_name}:category_index"
CATEGORY_DETAIL_VIEW = f"{app_name}:category_detail"
PROJECT_INDEX_VIEW = f"{app_name}:project_index"
PROJECT_DETAIL_VIEW = f"{app_name}:project_detail"
SUB_PROJECT_INDEX_VIEW = f"{app_name}:subproject_index"
SUB_PROJECT_DETAIL_VIEW = f"{app_name}:subproject_detail"


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
