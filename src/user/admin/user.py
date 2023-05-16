from django.contrib import admin

from shared.django_admins.base_admin import BaseModelAdmin
from user.models import User


@admin.register(User)
class UserAdmin(BaseModelAdmin):
    search_fields = [
        "username",
    ]
    autocomplete_fields = [
        "tenants",
    ]
