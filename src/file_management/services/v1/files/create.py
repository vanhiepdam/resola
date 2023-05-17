from django.core.files.base import ContentFile
from rest_framework.exceptions import PermissionDenied

from file_management.models import File
from tenant.models import Resource
from user.models import User


class CreateFileServiceV1:
    def __init__(self, file_name: str, resource: Resource, upload_by: User):
        self.file_name = file_name
        self.resource = resource
        self.upload_by = upload_by

    def validate(self) -> None:
        if self.resource.tenant not in self.upload_by.get_tenants():
            raise PermissionDenied("You do not have permission to upload to this tenant.")

    def create_new_file(self) -> File:
        dummy_file = ContentFile(content=b"", name=self.file_name)
        file: File = File.objects.create(
            file=dummy_file,
            resource=self.resource,
            uploaded_by=self.upload_by,
        )
        return file

    def execute(self) -> File:
        self.validate()
        file = self.create_new_file()
        return file
