from django.urls import path

from .views import (
    CategoryDetail,
    CategoryList,
    ProjectDetail,
    ProjectList,
    TimeRecordDetail,
    TimeRecordList,
)

app_name = "time_reporting"

urlpatterns = [
    path("v1/categories/", CategoryList.as_view(), name="category_index"),
    path(
        "v1/categories/<int:pk>/",
        CategoryDetail.as_view(),
        name="category_detail",
    ),
    path(
        "v1/projects/",
        ProjectList.as_view(),
        name="project_index",
    ),
    path(
        "v1/projects/<int:pk>/",
        ProjectDetail.as_view(),
        name="project_detail",
    ),
    path(
        "v1/records/",
        TimeRecordList.as_view(),
        name="record_index",
    ),
    path(
        "v1/records/<int:pk>/",
        TimeRecordDetail.as_view(),
        name="record_detail",
    ),
]
