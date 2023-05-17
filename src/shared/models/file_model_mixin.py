from django.conf import settings
from django.utils.module_loading import import_string


class FileModelMixin:
    def get_file_presigned_url(  # noqa: CFQ002
        self,
        field_name: str,
        has_read: bool = True,
        has_write: bool = False,
        has_create: bool = False,
        has_delete: bool = False,
    ) -> str:
        storage_provider_class = import_string(settings.FILE_MODEL_STORAGE_PROVIDER)
        return storage_provider_class().get_presign_url(  # type: ignore[no-any-return]
            blob_name=getattr(self, field_name).name,
            has_read=has_read,
            has_write=has_write,
            has_create=has_create,
            has_delete=has_delete,
        )

    def get_original_file_name(self, field_name: str) -> str:
        name: str = getattr(self, field_name).name.split("/")[-1]
        return name
