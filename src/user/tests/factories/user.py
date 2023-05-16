import factory
from django.db.models.signals import post_save
from factory.django import DjangoModelFactory

from user.models import User


@factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.LazyAttribute(lambda x: factory.Faker('name'))

    @factory.post_generation
    def tenants(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tenant in extracted:
                self.tenants.add(tenant)
