from __future__ import annotations

import logging

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as django_login
from django.db import transaction
from django.utils.translation import gettext_lazy as __
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.request import Request

from time_reporting.models import TimeRecord

log = logging.getLogger(__name__)
User = get_user_model()


@transaction.atomic
def create_user(
    username: str,
    email: str,
    password: str,
    super=False,
):
    log.info("Create User: %s", username)

    user_data = {
        "username": username,
        "email": email,
        "password": password,
    }

    if super:
        user = User.objects.create_superuser(**user_data)
    else:
        user = User.objects.create_user(**user_data)

    Token.objects.get_or_create(user=user)

    return user


def login_user(
    request: Request, username: str, password: str
) -> settings.AUTH_USER_MODEL:

    user = authenticate(request, username=username, password=password)
    if user is None:
        log.warning("Authentication failed for user: %s", username)
        raise AuthenticationFailed(__("Incorrect username or password"))

    log.debug("Authenticated user: %s", username)
    django_login(request, user)
    return user


def confirm_password(request: Request, password: str):
    user = authenticate(
        request, username=request.user.username, password=password
    )
    if user is None or user.pk != request.user.pk:
        raise AuthenticationFailed(__("Failed to confirm password"))


@transaction.atomic
def delete_user(username: str, request: Request | None = None):

    if request is not None and request.user.username == username:
        log.warning("Cannot delete the current user")
        raise PermissionDenied(__("Cannot delete the current user"))

    log.info("Deleting user %s", username)

    user = User.objects.filter(username=username).last()
    # Explicitly delete records for the user, since they are normally
    # protected
    TimeRecord.objects.filter(project__category__user=user).delete()
    user.delete()
