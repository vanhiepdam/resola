from rest_framework import serializers

from file_management.models import File
from file_management.services.v1.files.create import CreateFileServiceV1
from shared.restful.serializers import BaseModelSerializer
from tenant.models import Resource


class CreateFileResponseSerializerV1(BaseModelSerializer):
    presign_url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ["id", "presign_url"]

    def get_presign_url(self, instance: File) -> str:
        return instance.get_file_presigned_url(field_name="file", has_read=True, has_write=True)


class CreateFileSerializerV1(BaseModelSerializer):
    resource_id = serializers.PrimaryKeyRelatedField(
        queryset=Resource.objects.all().select_related("tenant"),
    )
    file_name = serializers.CharField(max_length=255)

    class Meta:
        model = File
        fields = ["file_name", "resource_id"]

    def create(self, validated_data: dict) -> File:
        service = CreateFileServiceV1(
            file_name=validated_data["file_name"],
            resource=validated_data["resource_id"],
            upload_by=self.context["request"].user,
        )
        file = service.execute()
        return file

    def to_representation(self, instance: File) -> dict:
        data: dict = CreateFileResponseSerializerV1(instance=instance).data
        return data
