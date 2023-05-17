from django.db import models

from shared.models.base_model import BaseModel


class Resource(BaseModel):
    tenant = models.ForeignKey("tenant.Tenant", on_delete=models.PROTECT, related_name="resources")
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name  # type: ignore[no-any-return]
