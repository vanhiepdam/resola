from django.contrib.auth.models import AbstractUser

from shared.models.base_model import BaseModel


class User(BaseModel, AbstractUser):
    pass
