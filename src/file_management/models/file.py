from django.db import models

from file_management.model_managers.file import FileManager
from shared.models.base_model import BaseModel
from shared.models.file_model_mixin import FileModelMixin
from shared.utilities.datetime import DateTimeUtil


def get_upload_to(instance, filename: str):  # type: ignore
    return "upload_files/{tenant}/{resource}/{filename}".format(
        tenant=instance.resource.tenant.code,
        resource=instance.resource.code,
        filename=filename,
    )


class File(BaseModel, FileModelMixin):
    file = models.FileField(upload_to=get_upload_to)
    resource = models.ForeignKey("tenant.Resource", on_delete=models.PROTECT, related_name="files")
    uploaded_by = models.ForeignKey("user.User", on_delete=models.PROTECT, related_name="files")
    uploaded_at = models.DateTimeField(default=DateTimeUtil.now)

    objects = FileManager()

    def __str__(self) -> str:
        name: str = self.file.name
        return name
