from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
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
    CanDeleteFilePermission,
    CanListFilePermission,
    CanRetrieveFilePermission,
    CanUploadFilePermission,
)
from file_management.restful.filters.file_filter import ListFileFilter
from file_management.serializers.v1.file.create import (
    CreateFileResponseSerializerV1,
    CreateFileSerializerV1,
)
from file_management.serializers.v1.file.list import ListFileSerializerV1
from file_management.serializers.v1.file.retrieve import RetrieveFileSerializerV1


class FileViewSetV1(
    GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ListFileFilter

    def get_queryset(self) -> QuerySet:
        return File.objects.all().filter_by_user_id(user_id=self.request.user.id).full_prefetch()

    def get_serializer_class(self):  # type: ignore  # noqa[CFQ004]
        if self.action == "list":
            return ListFileSerializerV1
        elif self.action == "retrieve":
            return RetrieveFileSerializerV1
        elif self.action == "create":
            return CreateFileSerializerV1
        return super().get_serializer_class()

    def get_permissions(self) -> list[BasePermission]:  # noqa[CFQ004]
        if self.action == "list":
            permission_classes = [CanListFilePermission | CanUploadFilePermission]
            return [permission() for permission in permission_classes]  # type: ignore[operator]
        elif self.action == "retrieve":
            permission_classes = [CanRetrieveFilePermission | CanUploadFilePermission]
            return [permission() for permission in permission_classes]  # type: ignore[operator]
        elif self.action == "destroy":
            permission_classes = [CanDeleteFilePermission]  # type: ignore[list-item]
            return [permission() for permission in permission_classes]  # type: ignore[operator]
        elif self.action == "create":
            permission_classes = [CanUploadFilePermission]  # type: ignore[list-item]
            return [permission() for permission in permission_classes]  # type: ignore[operator]
        return super().get_permissions()  # type: ignore[no-any-return]

    @extend_schema(responses=CreateFileResponseSerializerV1)
    def create(self, request, *args, **kwargs):  # type: ignore
        return super().create(request, *args, **kwargs)
