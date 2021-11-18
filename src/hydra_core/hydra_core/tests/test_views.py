import logging

from django.urls import reverse
import pytest
from rest_framework import status

from .factories import UserFactory

AUTH_LOGIN_VIEW = "login"
AUTH_CHECK_VIEW = "check"

log = logging.getLogger(__name__)


@pytest.mark.django_db
def test_login_user(anon_client):

    password = "quijibo"
    user = UserFactory(password=password)

    body = {
        "username": user.username,
        "password": password,
    }

    resp = anon_client.post(reverse(AUTH_LOGIN_VIEW), body, format="json")

    assert resp.status_code == status.HTTP_200_OK, resp.content
    assert resp.json() == {"authenticated": True}


@pytest.mark.django_db
def test_check_user(anon_client):
    password = "quijibo"
    user = UserFactory(password=password)

    anon_client.login(username=user.username, password=password)
    resp = anon_client.get(reverse(AUTH_CHECK_VIEW))

    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.json() == {
        "username": user.username,
        "email": user.email,
    }


@pytest.mark.django_db
def test_check_user_unauthenticated(anon_client):
    resp = anon_client.get(reverse(AUTH_CHECK_VIEW))
    assert resp.status_code == status.HTTP_403_FORBIDDEN, resp.content


@pytest.mark.django_db
def test_login_user_bad_password(anon_client):
    password = "quijibo"
    bad_password = "purple-monkey-dishwasher"

    user = UserFactory(password=password)

    body = {
        "username": user.username,
        "password": bad_password,
    }

    resp = anon_client.post(reverse(AUTH_LOGIN_VIEW), body, format="json")

    assert resp.status_code == status.HTTP_403_FORBIDDEN, resp.content


@pytest.mark.django_db
def test_login_user_bad_username(anon_client):
    password = "quijibo"

    UserFactory(username="test-user", password=password)

    body = {
        "username": "other-user",
        "password": password,
    }

    resp = anon_client.post(reverse(AUTH_LOGIN_VIEW), body, format="json")

    assert resp.status_code == status.HTTP_403_FORBIDDEN, resp.content
