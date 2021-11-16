from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as django_login
from django.db import transaction
from django.utils.translation import gettext_lazy as __
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

User = get_user_model()


@transaction.atomic
def create_user(
    username,
    email,
    password,
    super=False,
):
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
        raise AuthenticationFailed(__("Incorrect username or password"))
    django_login(request, user)
    return user


def confirm_password(request: Request, password: str):
    user = authenticate(
        request, username=request.user.username, password=password
    )
    if user is None or user.pk != request.user.pk:
        raise AuthenticationFailed(__("Failed to confirm password"))
