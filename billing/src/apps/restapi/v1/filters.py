from django_filters.rest_framework import DjangoFilterBackend


class UserFilterBackend(DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):
        user_id = request.data.get('user_id')
        return queryset.filter(user_id=user_id)
