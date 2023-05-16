# type: ignore
import pytest

from file_management.tests.factories.file import FileFactory
from tenant.tests.factories.tenant import TenantFactory
from user.tests.factories.user import UserFactory

pytestmark = [pytest.mark.django_db]


class TestListFileViewSetV1:
    def test_failed__user_is_not_authenticated(self, api_client):
        # given
        user = UserFactory()

        # when
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/v1/files")

        # then
        assert response.status_code == 401

    def test_failed__user_does_not_have_correct_permission(self, api_client):
        # given
        user = UserFactory()

        # when
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/v1/files")

        # then
        assert response.status_code == 403

    def test_success__user_has_correct_permission(self, api_client, mocker):
        # given user
        user = UserFactory()

        # give permission to user
        mocker.patch(
            "file_management.permissions.file_permissions.CanListFilePermission.has_permission",
            return_value=True,
        )

        # given files
        file = FileFactory(uploaded_by=user)

        # give noise files
        FileFactory(uploaded_by=UserFactory())

        # when
        api_client.force_authenticate(user=user)
        response = api_client.get("/api/v1/files")

        # then
        assert response.status_code == 200
        data = response.data
        assert len(data["results"]) == 1
        assert data["results"][0]["id"] == file.id

    def test_success__filter_by_tenant_id(self, api_client, mocker):
        # given user
        tenant_a = TenantFactory()
        tenant_b = TenantFactory()
        user = UserFactory(
            tenants=[
                tenant_a,
                tenant_b,
            ]
        )

        # give permission to user
        mocker.patch(
            "file_management.permissions.file_permissions.CanListFilePermission.has_permission",
            return_value=True,
        )

        # given files
        file = FileFactory(uploaded_by=user, resource__tenant=tenant_a)
        FileFactory(uploaded_by=user, resource__tenant=tenant_b)

        # give noise files
        FileFactory(uploaded_by=UserFactory())

        # when
        api_client.force_authenticate(user=user)
        response = api_client.get(f"/api/v1/files?tenant_id={tenant_a.id}")

        # then
        assert response.status_code == 200
        data = response.data
        assert len(data["results"]) == 1
        assert data["results"][0]["id"] == file.id
