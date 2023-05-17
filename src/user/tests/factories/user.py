import factory
from django.db.models.signals import post_save
from factory.django import DjangoModelFactory

from shared.utilities.text import TextUtil
from user.models import User


@factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.LazyAttribute(lambda x: TextUtil.generate_random_text())

    @factory.post_generation
    def tenants(self, create, extracted, **kwargs):  # type: ignore[no-untyped-def]
        if not create:
            return

        if extracted:
            for tenant in extracted:
                self.tenants.add(tenant)
