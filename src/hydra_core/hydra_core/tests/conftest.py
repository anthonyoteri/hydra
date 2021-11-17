import pytest
from rest_framework.test import APIClient

from .factories import UserFactory


def authenticate_client(
    client: APIClient, user
):  # pylint: disable=redefined-outer-name
    client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")
    return client


@pytest.fixture
@pytest.mark.django_db
def user():
    u = UserFactory()
    return u


@pytest.fixture
def client(user):  # pylint: disable=redefined-outer-name
    return authenticate_client(client=APIClient(), user=user)


@pytest.fixture
def anon_client():
    return APIClient()
