import factory
from django.db.models.signals import post_save
from factory.django import DjangoModelFactory

from tenant.models import Resource
from tenant.tests.factories.tenant import TenantFactory


@factory.django.mute_signals(post_save)
class ResourceFactory(DjangoModelFactory):
    class Meta:
        model = Resource
        django_get_or_create = ("code",)

    code = name = factory.LazyAttribute(lambda x: factory.Faker('name'))
    tenant = factory.SubFactory(TenantFactory)
