from rest_framework import serializers


class LikesSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30, required=True)
    link = serializers.URLField(required=True)
    count = serializers.IntegerField(min_value=1, required=True)
    email = serializers.EmailField(max_length=255)
