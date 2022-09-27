from apps.transactions.models import SubscriptionPeriods, Transaction
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
    period = serializers.CharField()
    periods_number = serializers.IntegerField()

    def validate_period(self, value):
        periods = SubscriptionPeriods.values
        if value not in periods:
            possible_values = ', '.join(periods)
            raise serializers.ValidationError(f'Possible values are: {possible_values}')
        return value


class RefundSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(required=True)
