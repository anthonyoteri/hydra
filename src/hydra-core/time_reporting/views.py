from django.contrib.auth import get_user_model
from django.db import transaction
from django.http.response import Http404
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import (
    BooleanField,
    CharField,
    DateTimeField,
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    Serializer,
    SerializerMethodField,
    SlugRelatedField,
)

from hydra_core.views import BaseAPIView

from . import services
from .models import Category, Project, TimeRecord

User = get_user_model()


class CategoryList(BaseAPIView):
    class OutputSerializer(Serializer):
        id = IntegerField()
        name = CharField()
        description = CharField(allow_null=True, allow_blank=True)
        num_records = SerializerMethodField()
        created = DateTimeField()
        updated = DateTimeField()

        def get_num_records(self, obj):
            return sum(p.records.count() for p in obj.projects.all())

    class InputSerializer(Serializer):
        name = CharField()
        description = CharField(allow_null=True, allow_blank=True)

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
        num_records = SerializerMethodField()

        def get_num_records(self, obj):
            return sum(p.records.count() for p in obj.projects.all())

        class Meta:
            model = Category
            fields = (
                "id",
                "name",
                "description",
                "num_records",
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
    class OutputSerializer(Serializer):
        id = IntegerField()
        category = PrimaryKeyRelatedField(queryset=Category.objects.all())
        name = CharField()
        description = CharField(allow_blank=True, allow_null=True)
        num_records = SerializerMethodField()
        created = DateTimeField()
        updated = DateTimeField()

        def get_num_records(self, obj):
            return obj.records.count()

    class InputSerializer(Serializer):
        name = CharField()
        category = PrimaryKeyRelatedField(queryset=Category.objects.all())
        description = CharField(allow_blank=True, allow_null=True)

    def get_queryset(self):
        return (
            Project.objects.filter(category__user=self.request.user)
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

        project = services.create_project(**serializer.validated_data)
        return Response(
            data=self.OutputSerializer(project).data,
            status=status.HTTP_201_CREATED,
        )


class ProjectDetail(BaseAPIView):
    class OutputSerializer(ModelSerializer):
        num_records = SerializerMethodField()

        def get_num_records(self, obj):
            return obj.records.count()

        class Meta:
            model = Project
            fields = (
                "id",
                "name",
                "category",
                "description",
                "num_records",
                "created",
                "updated",
            )

    class InputSerializer(ModelSerializer):
        class Meta:
            model = Project
            fields = ("category", "name", "category", "description")

    class PartialInputSerializer(Serializer):
        category = PrimaryKeyRelatedField(
            queryset=Category.objects.all(), required=False
        )
        name = CharField(required=False)
        slug = CharField(required=False)
        description = CharField(required=False)

    def get_object(self):
        obj = get_object_or_404(
            Project.objects.filter(category__user=self.request.user).all(),
            pk=self.kwargs["pk"],
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request: Request, pk: int, format=None) -> Response:
        project = self.get_object()
        return Response(data=self.OutputSerializer(project).data)

    def delete(self, request: Request, pk: int, format=None) -> Response:
        project = self.get_object()
        services.delete_project(pk=project.pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request: Request, pk: int, format=None) -> Response:
        project = self.get_object()
        serializer = self.InputSerializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            project = services.update_project(
                pk=pk, **serializer.validated_data
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
                pk=pk, **serializer.validated_data
            )
        except Project.DoesNotExist:
            raise Http404  # pylint: disable=raise-missing-from
        return Response(data=self.OutputSerializer(project).data)


class TimeRecordList(BaseAPIView):
    class OutputSerializer(Serializer):
        id = IntegerField()
        project = PrimaryKeyRelatedField(queryset=Project.objects.all())
        start_time = DateTimeField()
        stop_time = DateTimeField(allow_null=True)
        total_seconds = IntegerField()
        approved = BooleanField()

    class InputSerializer(Serializer):
        project = PrimaryKeyRelatedField(queryset=Project.objects.all())
        start_time = DateTimeField()
        stop_time = DateTimeField(required=False, allow_null=True)
        approved = BooleanField(required=False)

    def get_queryset(self):
        return (
            TimeRecord.objects.filter(
                project__category__user=self.request.user
            )
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

        record = services.create_record(**serializer.validated_data)

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
                "approved",
            )

    class InputSerializer(Serializer):
        project = PrimaryKeyRelatedField(queryset=Project.objects.all())
        start_time = DateTimeField()
        stop_time = DateTimeField(required=False, allow_null=True)
        approved = BooleanField()

    class PartialInputSerializer(Serializer):
        project = PrimaryKeyRelatedField(
            queryset=Project.objects.all(),
            required=False,
        )
        start_time = DateTimeField(required=False)
        stop_time = DateTimeField(required=False, allow_null=True)
        approved = BooleanField(required=False)

    def get_object(self):
        obj = get_object_or_404(
            TimeRecord.objects.filter(
                project__category__user=self.request.user
            ).all(),
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
            record = services.update_record(pk=pk, **serializer.validated_data)
        except TimeRecord.DoesNotExist:
            raise Http404  # pylint: disable=raise-missing-from

        return Response(data=self.OutputSerializer(record).data)

    def patch(self, request: Request, pk: int, format=None) -> Response:
        record = self.get_object()
        serializer = self.PartialInputSerializer(record, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            record = services.patch_record(pk=pk, **serializer.validated_data)
        except TimeRecord.DoesNotExist:
            raise Http404  # pylint: disable=raise-missing-from

        return Response(data=self.OutputSerializer(record).data)


class ConfigView(BaseAPIView):
    class InputSerializer(Serializer):
        class CategoryInputSerializer(CategoryList.InputSerializer):
            id = IntegerField()
            user = CharField()

        class ProjectInputSerializer(ProjectList.InputSerializer):
            id = IntegerField()
            category = IntegerField()

        class TimeRecordInputSerializer(TimeRecordList.InputSerializer):
            id = IntegerField()
            project = IntegerField()

        categories = CategoryInputSerializer(many=True)
        projects = ProjectInputSerializer(many=True)
        time_records = TimeRecordInputSerializer(many=True)

    class OutputSerializer(Serializer):
        class CategoryOutputSerializer(CategoryList.OutputSerializer):
            id = IntegerField()
            user = SlugRelatedField(
                slug_field="username", queryset=User.objects.all()
            )

        class ProjectOutputSerializer(ProjectList.OutputSerializer):
            id = IntegerField()

        class TimeRecordOutputSerializer(TimeRecordList.OutputSerializer):
            id = IntegerField()

        categories = CategoryOutputSerializer(many=True)
        projects = ProjectOutputSerializer(many=True)
        time_records = TimeRecordOutputSerializer(many=True)

    def get_serialized(self):
        config = {
            "categories": Category.objects.order_by("id"),
            "projects": Project.objects.order_by("id"),
            "time_records": TimeRecord.objects.order_by("id"),
        }
        return self.OutputSerializer(config).data

    def get(self, request: Request, format="json"):
        return Response(data=self.get_serialized())

    @transaction.atomic
    def put(self, request: Request, format="json"):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.import_config(serializer.validated_data)
        return Response()
