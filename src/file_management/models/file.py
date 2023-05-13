from django.db import models

from shared.models.base_model import BaseModel


class File(BaseModel):
    file = models.FileField(upload_to="uploads/")
    # todo: hiepdv: wait for confirmation from Everton in order to add the remaining fields

    def __str__(self) -> str:
        return self.file.name
