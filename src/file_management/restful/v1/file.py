from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import GenericViewSet

from file_management.models import File
from file_management.permissions.file_permissions import (
    CanListFilePermission,
    CanRetrieveFilePermission,
)
from file_management.restful.filters.file_filter import ListFileFilter
from file_management.serializers.v1.file.list import ListFileSerializerV1
from file_management.serializers.v1.file.retrieve import RetrieveFileSerializerV1


class FileViewSetV1(
    GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ListFileFilter

    def get_queryset(self) -> QuerySet:
        return File.objects.all().filter_by_user_id(user_id=self.request.user.id).full_prefetch()

    def get_serializer_class(self):  # type: ignore
        if self.action == "list":
            return ListFileSerializerV1
        elif self.action == "retrieve":
            return RetrieveFileSerializerV1
        return super().get_serializer_class()

    def get_permissions(self) -> list[BasePermission]:
        if self.action == "list":
            return [
                CanListFilePermission(),
            ]
        elif self.action == "retrieve":
            return [
                CanRetrieveFilePermission(),
            ]
        return super().get_permissions()  # type: ignore[no-any-return]
