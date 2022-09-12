from apps.offer.models import Subscription
from rest_framework import serializers


class SubscribeSerialize(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('guid', 'name', 'description', 'type', 'price', 'currency', )
