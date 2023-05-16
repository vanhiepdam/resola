import factory
from django.db.models.signals import post_save
from factory.django import DjangoModelFactory

from tenant.models import Tenant


@factory.django.mute_signals(post_save)
class TenantFactory(DjangoModelFactory):
    class Meta:
        model = Tenant
        django_get_or_create = ("code",)

    code = name = factory.LazyAttribute(lambda x: factory.Faker('name'))
