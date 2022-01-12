import logging

from dateutil.parser import isoparse
from django.conf import settings
from django.urls import reverse
from django.utils.timezone import localtime
import pytest
from rest_framework import status

from hydra_core.models import Settings

from .factories import UserFactory

ABOUT_VIEW = "about"
AUTH_LOGIN_VIEW = "login"
AUTH_CHECK_VIEW = "check"
SETTINGS_VIEW = "settings"

log = logging.getLogger(__name__)


@pytest.mark.django_db
def test_about_view(anon_client):
    resp = anon_client.get(reverse(ABOUT_VIEW))
    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.json() == {
        "app_version": settings.APP_VERSION,
        "timezone": settings.TIME_ZONE,
        "debug": settings.DEBUG,
        "build_date": localtime(isoparse(settings.BUILD_DATE)).isoformat(),
        "revision": settings.GIT_SHA,
    }


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
    assert resp.json() == {
        "username": user.username,
        "auth_token": str(user.auth_token.key),
    }


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


@pytest.mark.django_db
def test_settings_view_get(client):

    resp = client.get(reverse(SETTINGS_VIEW))
    assert resp.status_code == status.HTTP_200_OK, resp.content

    active_settings = Settings.objects.active()
    assert (
        resp.json()["retention_period_days"]
        == active_settings.retention_period_days
    )
    assert resp.json()["align_timestamps"] == active_settings.align_timestamps


@pytest.mark.django_db
def test_settings_view_put(client):
    current_settings = Settings.objects.active()

    body = {
        "retention_period_days": current_settings.retention_period_days + 1,
        "align_timestamps": not current_settings.align_timestamps,
    }

    resp = client.put(reverse(SETTINGS_VIEW), body, format="json")
    assert resp.status_code == status.HTTP_200_OK, resp.content

    assert resp.json() == body
