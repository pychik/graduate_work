from rest_framework import serializers


class ReceiverBaseSerializer(serializers.Serializer):
    """Базовый сериалайзер покупателей"""
    email = serializers.EmailField(max_length=255)
    first_name = serializers.CharField(max_length=30, required=False, allow_null=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_null=True)


class MovieBaseSerializer(serializers.Serializer):
    """Базовый сериалайзер произведений"""
    title = serializers.CharField(max_length=255)
    imdb_rating = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    url = serializers.URLField()


class ReceiverListSerializer(serializers.Serializer):
    receivers = ReceiverBaseSerializer(many=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        receivers = attrs.get('receivers', None)
        if not receivers:
            raise serializers.ValidationError({'receivers': 'Не может быть пустым!'})

        return attrs
