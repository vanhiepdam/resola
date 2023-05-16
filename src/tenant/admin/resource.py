from django.contrib import admin

from shared.django_admins.base_admin import BaseModelAdmin
from tenant.models import Resource


@admin.register(Resource)
class ResourceAdmin(BaseModelAdmin):
    search_fields = [
        "name",
    ]
