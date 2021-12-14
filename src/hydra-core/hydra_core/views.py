from typing import Tuple

from django.contrib.auth import get_user_model
from rest_framework import authentication, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import CharField, ModelSerializer, Serializer

from .auth import login_user
from .mixins import ExceptionHandlerMixin

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
