from typing import Tuple

from django.http.response import Http404
from rest_framework import authentication, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import (
    CharField,
    DateTimeField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    Serializer,
    SlugRelatedField,
)

from . import services
from .models import Category, Project, TimeRecord

AuthenticationClasses = Tuple[authentication.BaseAuthentication, ...]


class BaseAPIView(GenericAPIView):

    authentication_classes: AuthenticationClasses = (
        authentication.SessionAuthentication,
        authentication.TokenAuthentication,
    )


class CategoryList(BaseAPIView):
    class OutputSerializer(ModelSerializer):
        class Meta:
            model = Category
            fields = (
                "id",
                "name",
                "description",
                "created",
                "updated",
            )

    class InputSerializer(ModelSerializer):
        class Meta:
            model = Category
            fields = ("name", "description")

    def get_queryset(self):
        return (
            Category.objects.filter(user=self.request.user)
            .all()
            .order_by("created")
        )

    def head(self, request: Request, format=None) -> Response:
        queryset = self.get_queryset()
        count = queryset.count()
        return Response(headers={"X-Result-Count": count})

    def get(self, request: Request, format=None) -> Response:
        queryset = self.get_queryset()
        count = queryset.count()
        serializer = self.OutputSerializer(queryset, many=True)
        headers = {"X-Result-Count": count}
        return Response(data=serializer.data, headers=headers)

    def post(self, request: Request, format=None) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = services.create_category(
            user=request.user, **serializer.validated_data
        )
        return Response(
            data=self.OutputSerializer(category).data,
            status=status.HTTP_201_CREATED,
        )


class CategoryDetail(BaseAPIView):
    class OutputSerializer(ModelSerializer):
        class Meta:
            model = Category
            fields = (
                "id",
                "name",
                "description",
                "created",
                "updated",
            )

    class InputSerializer(ModelSerializer):
        class Meta:
            model = Category
            fields = ("name", "description")

    class PartialInputSerializer(Serializer):
        name = CharField(required=False)
        slug = CharField(required=False)
        description = CharField(required=False)

    def get_object(self):
        obj = get_object_or_404(
            Category.objects.filter(user=self.request.user).all(),
            pk=self.kwargs["pk"],
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request: Request, pk: int, format=None) -> Response:
        category = self.get_object()
        return Response(data=self.OutputSerializer(category).data)

    def delete(self, request: Request, pk: int, format=None) -> Response:
        services.delete_category(pk=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request: Request, pk: int, format=None) -> Response:
        category = self.get_object()
        serializer = self.InputSerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            category = services.update_category(
                pk=pk, user=request.user, **serializer.validated_data
            )
        except Category.DoesNotExist:
            raise Http404  # pylint: disable=raise-missing-from
        return Response(data=self.OutputSerializer(category).data)

    def patch(self, request: Request, pk: int, format=None) -> Response:
        category = self.get_object()
        serializer = self.PartialInputSerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            category = services.patch_category(
                pk=pk, user=request.user, **serializer.validated_data
            )
        except Category.DoesNotExist:
            raise Http404  # pylint: disable=raise-missing-from
        return Response(data=self.OutputSerializer(category).data)


class ProjectList(BaseAPIView):
    class OutputSerializer(ModelSerializer):
        class Meta:
            model = Project
            fields = (
                "id",
                "category",
                "name",
                "slug",
                "description",
                "created",
                "updated",
            )

        category = SlugRelatedField(
            queryset=Category.objects.all(), slug_field="name"
        )

    class InputSerializer(ModelSerializer):
        class Meta:
            model = Project
            fields = ("name", "slug", "category", "description")

    def get_queryset(self):
        return (
            Project.objects.filter(user=self.request.user)
            .all()
            .order_by("created")
        )

    def head(self, request: Request, format=None) -> Response:
        queryset = self.get_queryset()
        count = queryset.count()
        return Response(headers={"X-Result-Count": count})

    def get(self, request: Request, format=None) -> Response:
        queryset = self.get_queryset()
        count = queryset.count()
        serializer = self.OutputSerializer(queryset, many=True)
        headers = {"X-Result-Count": count}
        return Response(data=serializer.data, headers=headers)

    def post(self, request: Request, format=None) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project = services.create_project(
            user=request.user, **serializer.validated_data
        )
        return Response(
            data=self.OutputSerializer(project).data,
            status=status.HTTP_201_CREATED,
        )


class ProjectDetail(BaseAPIView):
    class OutputSerializer(ModelSerializer):
        class Meta:
            model = Project
            fields = (
                "id",
                "name",
                "slug",
                "category",
                "description",
                "created",
                "updated",
            )

        category = SlugRelatedField(
            queryset=Category.objects.all(), slug_field="name"
        )

    class InputSerializer(ModelSerializer):
        class Meta:
            model = Project
            fields = ("category", "name", "slug", "category", "description")

        category = PrimaryKeyRelatedField(queryset=Category.objects.all())

    class PartialInputSerializer(Serializer):
        category = PrimaryKeyRelatedField(
            queryset=Category.objects.all(), required=False
        )
        name = CharField(required=False)
        slug = CharField(required=False)
        description = CharField(required=False)

    def get_object(self):
        obj = get_object_or_404(
            Project.objects.filter(user=self.request.user).all(),
            pk=self.kwargs["pk"],
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request: Request, pk: int, format=None) -> Response:
        project = self.get_object()
        return Response(data=self.OutputSerializer(project).data)

    def delete(self, request: Request, pk: int, format=None) -> Response:
        services.delete_project(pk=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request: Request, pk: int, format=None) -> Response:
        project = self.get_object()
        serializer = self.InputSerializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            project = services.update_project(
                pk=pk, user=request.user, **serializer.validated_data
            )
        except Project.DoesNotExist:
            raise Http404  # pylint: disable=raise-missing-from
        return Response(data=self.OutputSerializer(project).data)

    def patch(self, request: Request, pk: int, format=None) -> Response:
        project = self.get_object()
        serializer = self.PartialInputSerializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            project = services.patch_project(
                pk=pk, user=request.user, **serializer.validated_data
            )
        except Project.DoesNotExist:
            raise Http404  # pylint: disable=raise-missing-from
        return Response(data=self.OutputSerializer(project).data)


class TimeRecordList(BaseAPIView):
    class OutputSerializer(ModelSerializer):
        class Meta:
            model = TimeRecord
            fields = (
                "id",
                "project",
                "start_time",
                "total_seconds",
                "stop_time",
            )

        project = SlugRelatedField(
            queryset=Project.objects.all(), slug_field="slug"
        )

    class InputSerializer(ModelSerializer):
        class Meta:
            model = TimeRecord
            fields = ("project", "start_time", "stop_time")

        project = SlugRelatedField(
            queryset=Project.objects.all(), slug_field="slug"
        )

    def get_queryset(self):
        return (
            TimeRecord.objects.filter(user=self.request.user)
            .all()
            .order_by("start_time")
        )

    def get(self, request: Request, format=None) -> Response:
        queryset = self.get_queryset()
        count = queryset.count()
        serializer = self.OutputSerializer(queryset, many=True)
        headers = {"X-Result-Count": count}
        return Response(data=serializer.data, headers=headers)

    def post(self, request: Request, format=None) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        record = services.create_record(
            user=request.user, **serializer.validated_data
        )

        return Response(
            data=self.OutputSerializer(record).data,
            status=status.HTTP_201_CREATED,
        )


class TimeRecordDetail(BaseAPIView):
    class OutputSerializer(ModelSerializer):
        class Meta:
            model = TimeRecord
            fields = (
                "id",
                "project",
                "start_time",
                "stop_time",
                "total_seconds",
            )

        project = SlugRelatedField(
            queryset=Project.objects.all(), slug_field="slug"
        )

    class InputSerializer(Serializer):
        project = SlugRelatedField(
            queryset=Project.objects.all(), slug_field="slug"
        )
        start_time = DateTimeField()
        stop_time = DateTimeField(required=False)

    class PartialInputSerializer(Serializer):
        project = SlugRelatedField(
            queryset=Project.objects.all(),
            slug_field="slug",
            required=False,
        )
        start_time = DateTimeField(required=False)
        stop_time = DateTimeField(required=False)

    def get_object(self):
        obj = get_object_or_404(
            TimeRecord.objects.filter(user=self.request.user).all(),
            pk=self.kwargs["pk"],
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request: Request, pk: int, format=None) -> Response:
        record = self.get_object()
        return Response(self.OutputSerializer(record).data)

    def delete(self, request: Request, pk: int, format=None) -> Response:
        record = self.get_object()
        services.delete_record(pk=record.pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request: Request, pk: int, format=None) -> Response:
        record = self.get_object()
        serializer = self.InputSerializer(record, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            record = services.update_record(
                pk=pk, user=request.user, **serializer.validated_data
            )
        except TimeRecord.DoesNotExist:
            raise Http404  # pylint: disable=raise-missing-from

        return Response(data=self.OutputSerializer(record).data)

    def patch(self, request: Request, pk: int, format=None) -> Response:
        record = self.get_object()
        serializer = self.PartialInputSerializer(record, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            record = services.patch_record(
                pk=pk, user=request.user, **serializer.validated_data
            )
        except TimeRecord.DoesNotExist:
            raise Http404  # pylint: disable=raise-missing-from

        return Response(data=self.OutputSerializer(record).data)
