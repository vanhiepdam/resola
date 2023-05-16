from file_management.models import File
from shared.restful.serializers import BaseModelSerializer
from tenant.models import Resource, Tenant
from user.models import User


class RetrieveFileResourceTenantSerializerV1(BaseModelSerializer):
    class Meta:
        model = Tenant
        fields = ["id", "code", "name"]


class RetrieveFileResourceSerializerV1(BaseModelSerializer):
    tenant = RetrieveFileResourceTenantSerializerV1()

    class Meta:
        model = Resource
        fields = ["id", "code", "name", "tenant"]


class RetrieveFileUserSerializerV1(BaseModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class RetrieveFileSerializerV1(BaseModelSerializer):
    resource = RetrieveFileResourceSerializerV1()
    uploaded_by = RetrieveFileUserSerializerV1()

    class Meta:
        model = File
        fields = ["id", "resource", "uploaded_by", "uploaded_at"]
