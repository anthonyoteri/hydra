from django.urls import path

from .views import (
    CategoryDetail,
    CategoryList,
    ProjectDetail,
    ProjectList,
    SubProjectDetail,
    SubProjectList,
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
        "v1/categories/<int:category_pk>/projects/",
        ProjectList.as_view(),
        name="project_index",
    ),
    path(
        "v1/categories/<int:category_pk>/projects/<int:pk>/",
        ProjectDetail.as_view(),
        name="project_detail",
    ),
    path(
        "v1/categories/*/projects/<int:project_pk>/sub_projects/",
        SubProjectList.as_view(),
        name="subproject_index",
    ),
    path(
        "v1/categories/*/projects/<int:project_pk>/sub_projects/<int:pk>/",
        SubProjectDetail.as_view(),
        name="subproject_detail",
    ),
]
