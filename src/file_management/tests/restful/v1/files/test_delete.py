# type: ignore
import pytest
from django.contrib.auth.models import Permission

from file_management.models import File
from file_management.tests.factories.file import FileFactory
from user.tests.factories.user import UserFactory

pytestmark = [pytest.mark.django_db]


class TestDeleteFileViewSetV1:
    def test_failed__user_is_not_authenticated(self, api_client):
        # given file
        file = FileFactory()

        # when
        response = api_client.delete(f"/api/v1/files/{file.id}")

        # then
        assert response.status_code == 403

    @pytest.mark.parametrize(
        "permission_codename",
        [
            "view_file",
            "add_file",
        ]
    )
    def test_failed__user_does_not_have_correct_permission(self, api_client, permission_codename):
        # given
        user = UserFactory()
        file = FileFactory()

        # give permission to user
        permissions = Permission.objects.filter(
            content_type__app_label="file_management",
            content_type__model="file",
            codename=permission_codename,
        )
        user.user_permissions.set(permissions)

        # when
        api_client.force_authenticate(user=user)
        response = api_client.delete(f"/api/v1/files/{file.id}")

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
            codename="delete_file",
        )
        user.user_permissions.set(permissions)

        # when
        api_client.force_authenticate(user=user)
        response = api_client.delete(f"/api/v1/files/{file.id}")

        # then
        assert response.status_code == 404

    def test_success__user_has_correct_permission(self, api_client):
        # given user
        user = UserFactory()

        # give permission to user
        permissions = Permission.objects.filter(
            content_type__app_label="file_management",
            content_type__model="file",
            codename="delete_file",
        )
        user.user_permissions.set(permissions)

        # given files
        file = FileFactory(uploaded_by=user)

        # give noise files
        FileFactory(uploaded_by=UserFactory())

        # when
        api_client.force_authenticate(user=user)
        response = api_client.delete(f"/api/v1/files/{file.id}")

        # then
        assert response.status_code == 204
        assert File.objects.filter(id=file.id).count() == 0
