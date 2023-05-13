# type: ignore
import pytest

from shared.storages.aws_s3 import AwsS3StorageProvider


class TestAwsS3StorageProvider:
    @pytest.mark.parametrize("has_read", [True, False])
    @pytest.mark.parametrize("has_write", [True, False])
    @pytest.mark.parametrize("has_create", [True, False])
    @pytest.mark.parametrize("has_delete", [True, False])
    @pytest.mark.parametrize("expire_seconds", [None, 300])
    def test_success__get_presigned_url(
            self, has_read, has_write, has_create, has_delete, expire_seconds, mocker
    ):
        # Arrange
        url_value = "https://test.txt"
        mocker.patch(
            "shared.storages.aws_s3.AwsS3StorageProvider._generate_presign_url",
            return_value=url_value,
        )

        # Act
        provider = AwsS3StorageProvider()
        url = provider.get_presign_url(
            "test.txt",
            has_read=has_read,
            has_write=has_write,
            has_create=has_create,
            has_delete=has_delete,
            expire_seconds=expire_seconds,
        )

        # Assert
        assert url == url_value
