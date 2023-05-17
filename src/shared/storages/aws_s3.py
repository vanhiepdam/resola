from typing import Any, Optional

import boto3
from django.conf import settings

from shared.storages.storage_provider import StorageProvider

READ_ACTION = "get_object"
WRITE_ACTION = "put_object"
CREATE_ACTION = "put_object"
DELETE_ACTION = "delete_object"


class AwsS3StorageProvider(StorageProvider):
    def __init__(self, bucket_name: str = settings.AWS_STORAGE_BUCKET_NAME) -> None:
        super().__init__()
        self.bucket_name = bucket_name

    def _init_client(self) -> Any:
        return boto3.client("s3")

    def _generate_presign_url(
        self,
        blob_name: str,
        action: str,
        expire_seconds: int,
    ) -> str:
        url: str = self.client.generate_presigned_url(
            action,
            Params={"Bucket": self.bucket_name, "Key": blob_name},
            ExpiresIn=expire_seconds,
        )
        return url

    def get_presign_url(  # noqa: CFQ002
        self,
        blob_name: str,
        has_read: bool = True,
        has_write: bool = False,
        has_create: bool = False,
        has_delete: bool = False,
        expire_seconds: Optional[int] = None,
    ) -> Optional[str]:
        if not expire_seconds:
            expire_seconds = self.expire_seconds

        # generate presign url
        action = None
        if has_read:
            action = READ_ACTION
        if has_write:
            action = WRITE_ACTION
        if has_create:
            action = CREATE_ACTION
        if has_delete:
            action = DELETE_ACTION
        if action is not None:
            return self._generate_presign_url(
                blob_name,
                action=action,
                expire_seconds=expire_seconds,
            )
        return None
