from abc import ABC


class StorageProvider(ABC):
    @staticmethod
    def get_presign_url(
        blob_name: str,
        has_read: bool = True,
        has_write: bool = False,
        has_add: bool = False,
        has_create: bool = False,
        has_delete: bool = False,
    ):
        pass
