from django.contrib.auth import get_user_model
from django.db import models

from shared.utilities.text import TextUtil

UserModel = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(
        UserModel,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        UserModel,
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
