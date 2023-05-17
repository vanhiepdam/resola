import factory
from django.db.models.signals import post_save
from factory.django import DjangoModelFactory

from file_management.models import File
from tenant.tests.factories.resource import ResourceFactory
from user.tests.factories.user import UserFactory


@factory.django.mute_signals(post_save)
class FileFactory(DjangoModelFactory):
    class Meta:
        model = File

    resource = factory.SubFactory(ResourceFactory)
    uploaded_by = factory.SubFactory(UserFactory)
    file = factory.django.FileField()
