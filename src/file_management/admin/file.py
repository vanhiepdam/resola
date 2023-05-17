from django.contrib import admin

from file_management.models import File
from shared.django_admins.base_admin import BaseModelAdmin


@admin.register(File)
class FileAdmin(BaseModelAdmin):
    search_fields = [
        "file___name",
    ]

    def get_queryset(self, request):  # type: ignore
        return super().get_queryset(request).full_prefetch()
