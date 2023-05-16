from django.contrib.auth.models import AbstractUser
from django.db import models

from shared.models.base_model import BaseModel


class User(BaseModel, AbstractUser):
    tenants = models.ManyToManyField(
        "tenant.Tenant",
        through="user.TenantUser",
        related_name="users",
        blank=True,
        through_fields=("user", "tenant"),
    )


class TenantUser(BaseModel):
    user = models.ForeignKey("user.User", on_delete=models.PROTECT, related_name="tenant_users")
    tenant = models.ForeignKey(
        "tenant.Tenant", on_delete=models.PROTECT, related_name="tenant_users"
    )

    def __str__(self) -> str:
        return f"{self.user.username} - {self.tenant.name}"
