from django.contrib import admin

from shared.django_admins.base_admin import BaseModelAdmin, BaseTabularInline
from user.models import User
from user.models.user import TenantUser


class UserTenantInline(BaseTabularInline):
    model = TenantUser
    extra = 0
    autocomplete_fields = ["tenant"]
    fk_name = "user"


@admin.register(User)
class UserAdmin(BaseModelAdmin):
    search_fields = [
        "username",
    ]
    autocomplete_fields = [
        "tenants",
    ]
    inlines = [UserTenantInline]
