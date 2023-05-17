from django.contrib import admin

from shared.django_admins.base_admin import BaseModelAdmin
from tenant.models import Tenant


@admin.register(Tenant)
class TenantAdmin(BaseModelAdmin):
    search_fields = [
        "name",
    ]
