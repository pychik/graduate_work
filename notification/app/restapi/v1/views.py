from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from restapi.v1.serializers.base import ReceiverBaseSerializer
from restapi.v1.serializers.bookmarks_serializer import BookmarksSerializer
from restapi.v1.serializers.like_serializer import LikesSerializer
from restapi.v1.serializers.movie_serializer import MovieSerializer


class LikesView(APIView):
    serializer_class = LikesSerializer

    @swagger_auto_schema(
        operation_description='Лайки.',
        request_body=LikesSerializer
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WelcomeView(APIView):
    serializer_class = ReceiverBaseSerializer

    @swagger_auto_schema(
        operation_description='Приветсвующее письмо.',
        request_body=ReceiverBaseSerializer
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookmarksView(APIView):
    serializer_class = BookmarksSerializer

    @swagger_auto_schema(
        operation_description="Закладки.",
        request_body=BookmarksSerializer
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieView(APIView):
    serializer_class = MovieSerializer

    @swagger_auto_schema(
        operation_description='Новый контент.',
        request_body=MovieSerializer
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
