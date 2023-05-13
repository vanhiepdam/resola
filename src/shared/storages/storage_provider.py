from abc import ABC, abstractmethod
from typing import Any, Optional


class StorageProvider(ABC):
    def __init__(self) -> None:
        self.client = self._init_client()
        self.expire_seconds = 300

    @abstractmethod
    def _init_client(self) -> Any:
        pass

    @abstractmethod
    def get_presign_url(  # noqa: CFQ002
        self,
        blob_name: str,
        has_read: bool = True,
        has_write: bool = False,
        has_create: bool = False,
        has_delete: bool = False,
        expire_seconds: Optional[int] = None
    ) -> str:
        pass
