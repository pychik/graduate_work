from django.core.paginator import Paginator
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from movies.api.v1.mixins import MoviesApiMixin


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50
    paginator_class = Paginator

    def get_context_data(self, *, object_list=None, **kwargs):
        qs = self.get_queryset()
        paginator, page, paginated_queryset, _ = self.paginate_queryset(qs, self.paginate_by)

        prev_page = None
        next_page = None

        if page.has_next():
            next_page = page.next_page_number()

        if page.has_previous():
            prev_page = page.previous_page_number()
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': prev_page,
            'next': next_page,
            'results': list(page.object_list)
        }

        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        context = self.get_object()
        return context
