from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from file_management.models import File
from file_management.restful.filters.file_filter import ListFileFilter


class FileViewSetV1(
    GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ListFileFilter

    def get_queryset(self) -> QuerySet:
        return File.objects.all().filter_by_user(user_id=self.request.user.id)
