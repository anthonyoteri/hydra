from django.utils import timezone
import factory
from factory.django import DjangoModelFactory
import factory.fuzzy

from ..models import Category, Project, SubProject, TimeRecord


class CategoryFactory(DjangoModelFactory):

    name = factory.Faker("slug")
    slug = factory.Faker("slug")
    description = factory.Faker("slug")

    class Meta:
        model = Category


class ProjectFactory(DjangoModelFactory):

    name = factory.Faker("slug")
    slug = factory.Faker("slug")
    description = factory.Faker("slug")

    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = Project


class SubProjectFactory(DjangoModelFactory):

    name = factory.Faker("slug")
    slug = factory.Faker("slug")
    description = factory.Faker("slug")

    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = SubProject


class TimeRecordFactory(DjangoModelFactory):

    sub_project = factory.SubFactory(SubProjectFactory)

    start_time = timezone.now().replace(microsecond=0)
    total_seconds = factory.fuzzy.FuzzyInteger(0, 86400)

    class Meta:
        model = TimeRecord
