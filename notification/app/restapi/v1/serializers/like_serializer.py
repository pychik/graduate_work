from rest_framework import serializers
from restapi.v1.serializers.base import ReceiverListSerializer


class LikesSerializer(ReceiverListSerializer):
    url = serializers.URLField()
    count = serializers.IntegerField(min_value=1)
