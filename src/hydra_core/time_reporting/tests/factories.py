from django.contrib.auth import get_user_model
from django.utils import timezone
import factory
from factory.django import DjangoModelFactory
import factory.fuzzy
from rest_framework.authtoken.models import Token

from time_reporting.models import Category, Project, TimeRecord

User = get_user_model()


class TokenFactory(DjangoModelFactory):
    class Meta:
        model = Token


class UserFactory(DjangoModelFactory):
    username = factory.Faker("user_name")
    password = factory.Faker("password")
    email = factory.Faker("email")

    token = factory.RelatedFactory(TokenFactory, "user")

    class Meta:
        model = User
        django_get_or_create = ("username",)


class CategoryFactory(DjangoModelFactory):

    name = factory.Faker("slug")
    description = factory.Faker("slug")

    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Category


class ProjectFactory(DjangoModelFactory):

    name = factory.Faker("slug")
    slug = factory.Faker("slug")
    description = factory.Faker("slug")

    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = Project


class TimeRecordFactory(DjangoModelFactory):

    project = factory.SubFactory(ProjectFactory)

    start_time = timezone.now().replace(microsecond=0)
    total_seconds = factory.fuzzy.FuzzyInteger(0, 86400)

    class Meta:
        model = TimeRecord
