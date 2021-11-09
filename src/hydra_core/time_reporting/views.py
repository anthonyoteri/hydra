from django.http.response import Http404
from rest_framework import status
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
from .models import Category, Project, SubProject, TimeRecord


class CategoryList(GenericAPIView):
    class OutputSerializer(ModelSerializer):
        class Meta:
            model = Category
            fields = (
                "id",
                "name",
                "slug",
                "description",
                "created",
                "updated",
            )

    class InputSerializer(ModelSerializer):
        class Meta:
            model = Category
            exclude = ("id", "created", "updated")

    def get_queryset(self):
        return Category.objects.all().order_by("created")

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

        category = services.create_category(**serializer.validated_data)
        return Response(
            data=self.OutputSerializer(category).data,
            status=status.HTTP_201_CREATED,
        )


class CategoryDetail(GenericAPIView):
    class OutputSerializer(ModelSerializer):
        class Meta:
            model = Category
            fields = (
                "id",
                "name",
                "slug",
                "description",
                "created",
                "updated",
            )

    class InputSerializer(ModelSerializer):
        class Meta:
            model = Category
            fields = ("name", "slug", "description")

    class PartialInputSerializer(Serializer):
        name = CharField(required=False)
        slug = CharField(required=False)
        description = CharField(required=False)

    def get_object(self):
        obj = get_object_or_404(
            Category.objects.all(),
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
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            category = services.update_category(
                pk=pk, **serializer.validated_data
            )
        except Category.DoesNotExist:
            raise Http404  # pylint: disable=raise-missing-from
        return Response(data=self.OutputSerializer(category).data)

    def patch(self, request: Request, pk: int, format=None) -> Response:
        serializer = self.PartialInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            category = services.patch_category(
                pk=pk, **serializer.validated_data
            )
        except Category.DoesNotExist:
            raise Http404  # pylint: disable=raise-missing-from
        return Response(data=self.OutputSerializer(category).data)


class ProjectList(GenericAPIView):
    class OutputSerializer(ModelSerializer):
        class Meta:
            model = Project
            fields = (
                "id",
                "name",
                "slug",
                "description",
                "created",
                "updated",
            )

    class InputSerializer(ModelSerializer):
        class Meta:
            model = Project
            fields = ("name", "slug", "description")

    def get_queryset(self):
        return (
            Project.objects.filter(category__pk=self.kwargs["category_pk"])
            .all()
            .order_by("created")
        )

    def get_category(self):
        obj = get_object_or_404(
            Category.objects.all(),
            pk=self.kwargs["category_pk"],
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def head(
        self, request: Request, category_pk: int, format=None
    ) -> Response:
        queryset = self.get_queryset()
        count = queryset.count()
        return Response(headers={"X-Result-Count": count})

    def get(self, request: Request, category_pk: int, format=None) -> Response:
        queryset = self.get_queryset()
        count = queryset.count()
        serializer = self.OutputSerializer(queryset, many=True)
        headers = {"X-Result-Count": count}
        return Response(data=serializer.data, headers=headers)

    def post(
        self, request: Request, category_pk: int, format=None
    ) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = self.get_category()

        project = services.create_project(
            category=category, **serializer.validated_data
        )
        return Response(
            data=self.OutputSerializer(project).data,
            status=status.HTTP_201_CREATED,
        )


class ProjectDetail(GenericAPIView):
    class OutputSerializer(ModelSerializer):
        class Meta:
            model = Project
            fields = (
                "id",
                "name",
                "slug",
                "description",
                "created",
                "updated",
            )

    class InputSerializer(ModelSerializer):
        class Meta:
            model = Project
            fields = ("category", "name", "slug", "description")

        category = PrimaryKeyRelatedField(
            queryset=Category.objects.all(), required=False
        )

    class PartialInputSerializer(Serializer):
        category = PrimaryKeyRelatedField(
            queryset=Category.objects.all(), required=False
        )
        name = CharField(required=False)
        slug = CharField(required=False)
        description = CharField(required=False)

    def get_category(self):
        obj = get_object_or_404(
            Category.objects.all(),
            pk=self.kwargs["category_pk"],
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get_object(self):
        obj = get_object_or_404(
            Project.objects.filter(
                category__pk=self.kwargs["category_pk"]
            ).all(),
            pk=self.kwargs["pk"],
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get(
        self, request: Request, category_pk: int, pk: int, format=None
    ) -> Response:
        project = self.get_object()
        return Response(data=self.OutputSerializer(project).data)

    def delete(
        self, request: Request, category_pk: int, pk: int, format=None
    ) -> Response:
        services.delete_project(pk=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(
        self, request: Request, category_pk: int, pk: int, format=None
    ) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            category = self.get_category()
            project = services.update_project(
                pk=pk, **{"category": category, **serializer.validated_data}
            )
        except Project.DoesNotExist:
            raise Http404  # pylint: disable=raise-missing-from
        return Response(data=self.OutputSerializer(project).data)

    def patch(
        self, request: Request, category_pk: int, pk: int, format=None
    ) -> Response:
        serializer = self.PartialInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            category = self.get_category()
            project = services.patch_project(
                pk=pk, **{"category": category, **serializer.validated_data}
            )
        except Project.DoesNotExist:
            raise Http404  # pylint: disable=raise-missing-from
        return Response(data=self.OutputSerializer(project).data)


class SubProjectList(GenericAPIView):
    class OutputSerializer(ModelSerializer):
        class Meta:
            model = SubProject
            fields = (
                "id",
                "name",
                "slug",
                "description",
                "created",
                "updated",
            )

    class InputSerializer(ModelSerializer):
        class Meta:
            model = SubProject
            fields = ("name", "slug", "description")

    def get_queryset(self):
        return (
            SubProject.objects.filter(project__pk=self.kwargs["project_pk"])
            .all()
            .order_by("created")
        )

    def get_project(self):
        obj = get_object_or_404(
            Project.objects.all(),
            pk=self.kwargs["project_pk"],
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def head(self, request: Request, project_pk: int, format=None) -> Response:
        queryset = self.get_queryset()
        count = queryset.count()
        return Response(headers={"X-Result-Count": count})

    def get(self, request: Request, project_pk: int, format=None) -> Response:
        queryset = self.get_queryset()
        count = queryset.count()
        serializer = self.OutputSerializer(queryset, many=True)
        headers = {"X-Result-Count": count}
        return Response(data=serializer.data, headers=headers)

    def post(self, request: Request, project_pk: int, format=None) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project = self.get_project()

        project = services.create_sub_project(
            project=project, **serializer.validated_data
        )
        return Response(
            data=self.OutputSerializer(project).data,
            status=status.HTTP_201_CREATED,
        )


class SubProjectDetail(GenericAPIView):
    class OutputSerializer(ModelSerializer):
        class Meta:
            model = SubProject
            fields = (
                "id",
                "name",
                "slug",
                "description",
                "created",
                "updated",
            )

    class InputSerializer(ModelSerializer):
        class Meta:
            model = SubProject
            fields = ("project", "name", "slug", "description")

        project = PrimaryKeyRelatedField(
            queryset=Project.objects.all(), required=False
        )

    class PartialInputSerializer(Serializer):
        project = PrimaryKeyRelatedField(
            queryset=Project.objects.all(), required=False
        )
        name = CharField(required=False)
        slug = CharField(required=False)
        description = CharField(required=False)

    def get_project(self):
        obj = get_object_or_404(
            Project.objects.all(),
            pk=self.kwargs["project_pk"],
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get_object(self):
        obj = get_object_or_404(
            SubProject.objects.filter(
                project__pk=self.kwargs["project_pk"]
            ).all(),
            pk=self.kwargs["pk"],
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def get(
        self,
        request: Request,
        project_pk: int,
        pk: int,
        format=None,
    ) -> Response:
        sub_project = self.get_object()
        return Response(data=self.OutputSerializer(sub_project).data)

    def delete(
        self,
        request: Request,
        project_pk: int,
        pk: int,
        format=None,
    ) -> Response:
        services.delete_sub_project(pk=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(
        self,
        request: Request,
        project_pk: int,
        pk: int,
        format=None,
    ) -> Response:
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            project = self.get_project()
            sub_project = services.update_sub_project(
                pk=pk, **{"project": project, **serializer.validated_data}
            )
        except Project.DoesNotExist:
            raise Http404  # pylint: disable=raise-missing-from
        return Response(data=self.OutputSerializer(sub_project).data)

    def patch(
        self,
        request: Request,
        project_pk: int,
        pk: int,
        format=None,
    ) -> Response:
        serializer = self.PartialInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            project = self.get_project()
            sub_project = services.patch_sub_project(
                pk=pk, **{"project": project, **serializer.validated_data}
            )
        except Project.DoesNotExist:
            raise Http404  # pylint: disable=raise-missing-from
        return Response(data=self.OutputSerializer(sub_project).data)


class TimeRecordList(GenericAPIView):
    class OutputSerializer(ModelSerializer):
        class Meta:
            model = TimeRecord
            fields = (
                "id",
                "sub_project",
                "start_time",
                "total_seconds",
                "stop_time",
            )

        sub_project = SlugRelatedField(
            queryset=SubProject.objects.all(), slug_field="slug"
        )

    class InputSerializer(ModelSerializer):
        class Meta:
            model = TimeRecord
            fields = ("sub_project", "start_time", "stop_time")

        sub_project = SlugRelatedField(
            queryset=SubProject.objects.all(), slug_field="slug"
        )

    def get_queryset(self):
        return TimeRecord.objects.all().order_by("start_time")

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


class TimeRecordDetail(GenericAPIView):
    class OutputSerializer(ModelSerializer):
        class Meta:
            model = TimeRecord
            fields = (
                "id",
                "sub_project",
                "start_time",
                "stop_time",
                "total_seconds",
            )

        sub_project = SlugRelatedField(
            queryset=SubProject.objects.all(), slug_field="slug"
        )

    class InputSerializer(Serializer):
        sub_project = SlugRelatedField(
            queryset=SubProject.objects.all(), slug_field="slug"
        )
        start_time = DateTimeField()
        stop_time = DateTimeField(required=False)

    class PartialInputSerializer(Serializer):
        sub_project = SlugRelatedField(
            queryset=SubProject.objects.all(),
            slug_field="slug",
            required=False,
        )
        start_time = DateTimeField(required=False)
        stop_time = DateTimeField(required=False)

    def get_object(self):
        obj = get_object_or_404(
            TimeRecord.objects.all(),
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
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            record = services.update_record(pk=pk, **serializer.validated_data)
        except TimeRecord.DoesNotExist:
            raise Http404  # pylint: disable=raise-missing-from

        return Response(data=self.OutputSerializer(record).data)

    def patch(self, request: Request, pk: int, format=None) -> Response:
        serializer = self.PartialInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            record = services.patch_record(pk=pk, **serializer.validated_data)
        except TimeRecord.DoesNotExist:
            raise Http404  # pylint: disable=raise-missing-from

        return Response(data=self.OutputSerializer(record).data)
