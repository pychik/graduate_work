from rest_framework import serializers


class NewTransactionSerializer(serializers.Serializer):
    subscription_id = serializers.UUIDField(required=True)
    user_id = serializers.CharField(max_length=36, required=True)
