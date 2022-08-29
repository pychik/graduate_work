from rest_framework import serializers
from restapi.v1.serializers.base import MovieBaseSerializer, ReceiverListSerializer


class BookmarksSerializer(ReceiverListSerializer):
    url = serializers.URLField()
    count = serializers.IntegerField(min_value=1)
    movies = MovieBaseSerializer(many=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        movies = attrs.get('movies', None)

        if not movies:
            raise serializers.ValidationError({'movies': 'Не должно быть пустым!'})

        return attrs
