from django.shortcuts import reverse
from django.utils.http import urlencode


def reverse_with_query_params(viewname, kwargs=None, query_params=None):
    url = reverse(viewname, kwargs=kwargs)

    if query_params:
        return f'{url}?{urlencode(query_params)}'

    return url
