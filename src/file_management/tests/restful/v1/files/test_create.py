# type: ignore
import pytest
from django.contrib.auth.models import Permission

from file_management.tests.factories.file import FileFactory
from tenant.tests.factories.resource import ResourceFactory
from tenant.tests.factories.tenant import TenantFactory
from user.tests.factories.user import UserFactory

pytestmark = [pytest.mark.django_db]


class TestCreateFileViewSetV1:
    def test_failed__user_is_not_authenticated(self, api_client):
        # when
        response = api_client.post("/api/v1/files")

        # then
        assert response.status_code == 403

    @pytest.mark.parametrize(
        "permission_codename",
        [
            "view_file",
            "delete_file",
        ],
    )
    def test_failed__user_does_not_have_correct_permission(self, api_client, permission_codename):
        # given
        user = UserFactory()

        # give permission to user
        permissions = Permission.objects.filter(
            content_type__app_label="file_management",
            content_type__model="file",
            codename=permission_codename,
        )
        user.user_permissions.set(permissions)

        # when
        api_client.force_authenticate(user=user)
        response = api_client.post("/api/v1/files")

        # then
        assert response.status_code == 403

    @pytest.mark.parametrize(
        "permission_codename",
        [
            "add_file",
        ],
    )
    def test_failed__user_has_correct_permission__but_upload_to_a_tenant_they_are_not_in(
        self, api_client, permission_codename
    ):
        # given data
        tenant = TenantFactory()
        ResourceFactory(tenant=tenant)
        user = UserFactory(tenants=[tenant])

        # given noise data
        tenant_b = TenantFactory()
        resource_b = ResourceFactory(tenant=tenant_b)

        # give permission to user
        permissions = Permission.objects.filter(
            content_type__app_label="file_management",
            content_type__model="file",
            codename=permission_codename,
        )
        user.user_permissions.set(permissions)

        # payload
        payload = {
            "resource_id": resource_b.id,
            "file_name": "test_file_name",
        }

        # when
        api_client.force_authenticate(user=user)
        response = api_client.post("/api/v1/files", data=payload, format="json")

        # then
        assert response.status_code == 403
        assert response.json() == {"detail": "You do not have permission to perform this action."}

    @pytest.mark.parametrize(
        "permission_codename",
        [
            "add_file",
        ],
    )
    def test_success__user_has_correct_permission__upload_to_proper_tenant(
        self, api_client, permission_codename, mocker
    ):
        # given data
        tenant = TenantFactory()
        resource = ResourceFactory(tenant=tenant)
        user = UserFactory(tenants=[tenant])

        # give permission to user
        permissions = Permission.objects.filter(
            content_type__app_label="file_management",
            content_type__model="file",
            codename=permission_codename,
        )
        user.user_permissions.set(permissions)

        # payload
        payload = {
            "resource_id": resource.id,
            "file_name": "test_file_name",
        }

        # mock presign url
        mocker.patch(
            "shared.storages.aws_s3.AwsS3StorageProvider.get_presign_url",
            return_value="https://test.com",
        )

        # when
        api_client.force_authenticate(user=user)
        response = api_client.post("/api/v1/files", data=payload, format="json")

        # then
        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["presign_url"] == "https://test.com"

    @pytest.mark.parametrize(
        "permission_codename",
        [
            "add_file",
        ],
    )
    def test_success__user_are_in_multiple_tenants(self, api_client, permission_codename):
        # given user
        tenant_a = TenantFactory()
        tenant_b = TenantFactory()
        user = UserFactory(
            tenants=[
                tenant_a,
                tenant_b,
            ]
        )
        resource = ResourceFactory(tenant=tenant_a)

        # give permission to user
        permissions = Permission.objects.filter(
            content_type__app_label="file_management",
            content_type__model="file",
            codename=permission_codename,
        )
        user.user_permissions.set(permissions)

        # given files
        file = FileFactory(uploaded_by=user, resource__tenant=tenant_a)
        FileFactory(uploaded_by=user, resource__tenant=tenant_b)

        # give noise files
        FileFactory(uploaded_by=UserFactory())

        # payload
        payload = {
            "resource_id": resource.id,
            "file_name": "test_file_name",
        }

        # when
        api_client.force_authenticate(user=user)
        response = api_client.post(f"/api/v1/files", data=payload, format="json")

        # then
        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["presign_url"] == "https://test.com"
