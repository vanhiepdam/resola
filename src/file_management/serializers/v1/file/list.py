from file_management.models import File
from shared.restful.serializers import BaseModelSerializer
from tenant.models import Resource, Tenant
from user.models import User


class ListFileResourceTenantSerializerV1(BaseModelSerializer):
    class Meta:
        model = Tenant
        fields = ["id", "code", "name"]


class ListFileResourceSerializerV1(BaseModelSerializer):
    tenant = ListFileResourceTenantSerializerV1()

    class Meta:
        model = Resource
        fields = ["id", "code", "name", "tenant"]


class ListFileUserSerializerV1(BaseModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class ListFileSerializerV1(BaseModelSerializer):
    resource = ListFileResourceSerializerV1()
    uploaded_by = ListFileUserSerializerV1()

    class Meta:
        model = File
        fields = ["id", "resource", "uploaded_by", "uploaded_at"]
