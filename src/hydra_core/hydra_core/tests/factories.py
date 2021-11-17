from django.contrib.auth import get_user_model
import factory
from factory.django import DjangoModelFactory
import factory.fuzzy

from hydra_core.auth import create_user

User = get_user_model()


class UserFactory(DjangoModelFactory):
    username = factory.Faker("user_name")
    password = factory.Faker("password")
    email = factory.Faker("email")

    class Meta:
        model = User
        django_get_or_create = ("username",)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return create_user(*args, **kwargs)
