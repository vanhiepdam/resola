# type: ignore
import pytest

from tenant.tests.factories.tenant import TenantFactory
from user.tests.factories.user import UserFactory

pytestmark = [pytest.mark.django_db]


class TestUserModel:
    def test_success__get_tenants(self):
        # given tenants
        tenant_a = TenantFactory()
        tenant_b = TenantFactory()
        tenant_c = TenantFactory()

        # given user
        user = UserFactory(tenants=[tenant_a, tenant_b])

        # when
        tenants = user.get_tenants()

        # then
        assert len(tenants) == 2
        assert tenant_a in tenants
        assert tenant_b in tenants
        assert tenant_c not in tenants
