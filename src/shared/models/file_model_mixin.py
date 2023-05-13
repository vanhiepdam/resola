from shared.storages.storage_provider import StorageProvider


class FileModelMixin:
    storage_provider: StorageProvider = None

    def get_file_presigned_url(  # noqa: CFQ002
        self,
        field_name: str,
        has_read: bool = True,
        has_write: bool = False,
        has_add: bool = False,
        has_create: bool = False,
        has_delete: bool = False,
    ) -> str:
        return self.storage_provider.get_presign_url(
            blob_name=getattr(self, field_name).name,
            has_read=has_read,
            has_write=has_write,
            has_add=has_add,
            has_create=has_create,
            has_delete=has_delete,
        )

    def get_original_file_name(self, field_name: str) -> str:
        name: str = getattr(self, field_name).name.split("/")[-1]
        return name
