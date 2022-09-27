from flask import url_for


def get_endpoint_url(name: str, pk=None) -> str:
    kwargs = {'pk': pk}
    return url_for(f'api.{name}', **kwargs)
