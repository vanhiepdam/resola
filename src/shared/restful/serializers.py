from rest_framework.serializers import ModelSerializer, Serializer


class BaseModelSerializer(ModelSerializer):
    pass


class ArbitrarySerializer(Serializer):
    def update(self, instance, validated_data):  # type: ignore
        pass

    def create(self, validated_data):  # type: ignore
        pass
