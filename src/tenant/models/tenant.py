from django.db import models

from shared.models.base_model import BaseModel


class Tenant(BaseModel):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name  # type: ignore[no-any-return]
