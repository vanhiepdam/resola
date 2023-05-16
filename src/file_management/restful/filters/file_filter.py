from django.db.models import QuerySet
from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError

from file_management.models import File


class ListFileFilter(filters.FilterSet):
    tenant_id = filters.CharFilter(method="filter_tenant")

    class Meta:
        model = File
        fields = ["tenant_id"]

    def filter_tenant(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        if not value.isdigit():
            raise ValidationError("tenant_id must be a number")

        return queryset.filter(resource__tenant_id=int(value))
