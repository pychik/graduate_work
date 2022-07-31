from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from movies.models import Filmwork, PersonFilmWork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        roles_enum = PersonFilmWork.RoleTypes
        qs = self.model.objects.all().values(). \
            annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=ArrayAgg('persons__full_name',
                            filter=(Q(personfilmwork__role=roles_enum.actor)),
                            distinct=True),
            directors=ArrayAgg('persons__full_name',
                               filter=(Q(personfilmwork__role=roles_enum.director)),
                               distinct=True),
            writers=ArrayAgg('persons__full_name',
                             filter=(Q(personfilmwork__role=roles_enum.writer)),
                             distinct=True),
        )
        return qs

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
