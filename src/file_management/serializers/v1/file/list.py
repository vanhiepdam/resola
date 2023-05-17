from rest_framework import serializers

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
    file_name = serializers.SerializerMethodField()
    presigned_url = serializers.SerializerMethodField()
    resource = ListFileResourceSerializerV1()
    uploaded_by = ListFileUserSerializerV1()

    class Meta:
        model = File
        fields = ["id", "file_name", "presigned_url", "resource", "uploaded_by", "uploaded_at"]

    def get_file_name(self, obj: File) -> str:
        return obj.get_original_file_name("file")

    def get_presigned_url(self, obj: File) -> str:
        return obj.get_file_presigned_url("file", has_read=True)
