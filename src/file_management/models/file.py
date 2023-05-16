from django.db import models

from file_management.model_managers.file import FileManager
from shared.models.base_model import BaseModel
from shared.utilities.datetime import DateTimeUtil


class File(BaseModel):
    file = models.FileField(upload_to="uploads/")
    resource = models.ForeignKey("tenant.Resource", on_delete=models.PROTECT, related_name="files")
    uploaded_by = models.ForeignKey("user.User", on_delete=models.PROTECT, related_name="files")
    uploaded_at = models.DateTimeField(default=DateTimeUtil.now)

    objects = FileManager()

    def __str__(self) -> str:
        name: str = self.file.name
        return name
