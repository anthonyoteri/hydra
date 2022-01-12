from typing import Tuple

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import (
    BooleanField,
    CharField,
    DateTimeField,
    IntegerField,
    ModelSerializer,
    Serializer,
)

from .auth import login_user
from .mixins import ExceptionHandlerMixin
from .models import Settings
from .services import update_settings

User = get_user_model()
AuthenticationClasses = Tuple[authentication.BaseAuthentication, ...]
PermissionClasses = Tuple[permissions.BasePermission, ...]


class BaseAPIView(ExceptionHandlerMixin, GenericAPIView):

    authentication_classes: AuthenticationClasses = (
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes: PermissionClasses = (permissions.IsAuthenticated,)


class BasePublicAPIView(ExceptionHandlerMixin, GenericAPIView):
    authentication_classes: AuthenticationClasses = ()
    permission_classes: PermissionClasses = ()


class AboutView(BasePublicAPIView):
    class OutputSerializer(Serializer):
        app_version = CharField()
        timezone = CharField()
        debug = BooleanField()
        build_date = DateTimeField()
        revision = CharField(allow_null=True)

    def get_data(self):
        about = {
            "app_version": settings.APP_VERSION,
            "timezone": settings.TIME_ZONE,
            "debug": settings.DEBUG,
            "build_date": settings.BUILD_DATE,
            "revision": settings.GIT_SHA,
        }
        serializer = self.OutputSerializer(data=about)
        serializer.is_valid(raise_exception=True)

        return serializer.data

    def get(self, request: Request, format=None):
        return Response(self.get_data())


class LoginView(BasePublicAPIView):
    class InputSerializer(Serializer):
        username = CharField()
        password = CharField(style={"input_type": "password"})

    class OutputSerializer(Serializer):
        username = CharField()
        auth_token = CharField()

    def post(self, request: Request, format=None) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = login_user(request, **serializer.validated_data)

        return Response(self.OutputSerializer(user).data)


class UserDetail(BaseAPIView):
    class OutputSerializer(ModelSerializer):
        class Meta:
            model = User
            fields = ("username", "email")

    def get(self, request: Request, format=None) -> Response:
        serializer = self.OutputSerializer(request.user)
        return Response(data=serializer.data)


class SettingsView(BaseAPIView):
    class OutputSerializer(Serializer):
        retention_period_days = IntegerField()
        align_timestamps = BooleanField()

    class InputSerializer(Serializer):
        retention_period_days = IntegerField(required=False)
        align_timestamps = BooleanField(required=False)

    def get_queryset(self):
        return Settings.objects.active()

    def get(self, request: Request, format=None) -> Response:
        queryset = self.get_queryset()
        return Response(self.OutputSerializer(queryset).data)

    def put(self, request: Request, format=None) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_settings(serializer.validated_data)
        return Response(self.OutputSerializer(self.get_queryset()).data)
