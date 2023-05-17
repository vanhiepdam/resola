# type: ignore
import pytest
from django.contrib.auth.models import Permission

from file_management.tests.factories.file import FileFactory
from user.tests.factories.user import UserFactory

pytestmark = [pytest.mark.django_db]


class TestRetrieveFileViewSetV1:
    def test_failed__user_is_not_authenticated(self, api_client):
        # given file
        file = FileFactory()

        # when
        response = api_client.get(f"/api/v1/files/{file.id}")

        # then
        assert response.status_code == 401

    def test_failed__user_does_not_have_correct_permission(self, api_client):
        # given
        user = UserFactory()
        file = FileFactory()

        # when
        api_client.force_authenticate(user=user)
        response = api_client.get(f"/api/v1/files/{file.id}")

        # then
        assert response.status_code == 403

    def test_failed__filter_by_file_of_others(self, api_client):
        # given
        user = UserFactory()
        file = FileFactory(uploaded_by=UserFactory())

        # give permission to user
        permissions = Permission.objects.filter(
            content_type__app_label="file_management",
            content_type__model="file",
            codename="view_file",
        )
        user.user_permissions.set(permissions)

        # when
        api_client.force_authenticate(user=user)
        response = api_client.get(f"/api/v1/files/{file.id}")

        # then
        assert response.status_code == 404

    @pytest.mark.parametrize(
        "permission_codename",
        [
            "view_file",
            "add_file",
        ]
    )
    def test_success__user_has_correct_permission(self, api_client, permission_codename, mocker):
        # given user
        user = UserFactory()

        # give permission to user
        permissions = Permission.objects.filter(
            content_type__app_label="file_management",
            content_type__model="file",
            codename=permission_codename,
        )
        user.user_permissions.set(permissions)

        # given files
        file = FileFactory(uploaded_by=user)

        # give noise files
        FileFactory(uploaded_by=UserFactory())

        # mock data
        url_value = "https://test.txt"
        mocker.patch(
            "shared.storages.aws_s3.AwsS3StorageProvider._generate_presign_url",
            return_value=url_value,
        )

        # when
        api_client.force_authenticate(user=user)
        response = api_client.get(f"/api/v1/files/{file.id}")

        # then
        assert response.status_code == 200
        data = response.data
        assert data["id"] == file.id
        assert data["file_name"] == file.get_original_file_name("file")
        assert data["presigned_url"] == url_value

        assert data["uploaded_by"]["id"] == user.id
        assert data["uploaded_by"]["username"] == user.username

        assert data["resource"]["id"] == file.resource.id
        assert data["resource"]["code"] == file.resource.code
        assert data["resource"]["name"] == file.resource.name

        assert data["resource"]["tenant"]["id"] == file.resource.tenant.id
        assert data["resource"]["tenant"]["code"] == file.resource.tenant.code
        assert data["resource"]["tenant"]["name"] == file.resource.tenant.name
