import factory
from django.db.models.signals import post_save
from factory.django import DjangoModelFactory

from shared.utilities.text import TextUtil
from tenant.models import Resource
from tenant.tests.factories.tenant import TenantFactory


@factory.django.mute_signals(post_save)
class ResourceFactory(DjangoModelFactory):
    class Meta:
        model = Resource
        django_get_or_create = ("code",)

    code = name = factory.LazyAttribute(lambda x: TextUtil.generate_random_text())
    tenant = factory.SubFactory(TenantFactory)
