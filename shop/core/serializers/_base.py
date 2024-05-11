from rest_framework import serializers


class UUIDSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=False)


class CountSerializer(serializers.Serializer):
    count = serializers.IntegerField(required=True)
