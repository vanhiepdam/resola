from django.db import models

from main import settings
from shared.utilities.text import TextUtil


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_updated",
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True
        ordering = ["id"]

    def update_fields(self, **kwargs) -> None:  # type: ignore
        self.__class__.objects.filter(pk=self.pk).update(**kwargs)


class BaseUUIDModel(BaseModel):
    id = models.UUIDField(
        default=TextUtil.generate_uuid,
        primary_key=True,
        unique=True,
    )

    class Meta:
        abstract = True
