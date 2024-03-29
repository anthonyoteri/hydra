"""hydra_core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from .views import AboutView, LoginView, SettingsView, UserDetail

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/auth/login/", LoginView.as_view(), name="login"),
    path("v1/auth/check/", UserDetail.as_view(), name="check"),
    path("v1/about/", AboutView.as_view(), name="about"),
    path("v1/settings/", SettingsView.as_view(), name="settings"),
    path("", include("time_reporting.urls")),
]
