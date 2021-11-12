from django.utils import timezone
import factory
from factory.django import DjangoModelFactory
import factory.fuzzy

from ..models import Category, Project, TimeRecord


class CategoryFactory(DjangoModelFactory):

    name = factory.Faker("slug")
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


class TimeRecordFactory(DjangoModelFactory):

    project = factory.SubFactory(ProjectFactory)

    start_time = timezone.now().replace(microsecond=0)
    total_seconds = factory.fuzzy.FuzzyInteger(0, 86400)

    class Meta:
        model = TimeRecord
