from apps.transactions.models import Transaction
from rest_framework import serializers


class TransactionSerializer(serializers.ModelSerializer):
    subscription = serializers.CharField(source='subscription.name', read_only=True)

    class Meta:
        model = Transaction
        fields = ['guid', 'user_id', 'status', 'subscription']


class UserIdSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=36, required=True)


class NewTransactionSerializer(UserIdSerializer):
    subscription_id = serializers.UUIDField(required=True)
