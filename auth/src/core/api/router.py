from core.base import ExternalAPIRouter


class APIRouter(ExternalAPIRouter):
    def get_base_endpoint(self):
        credentials = self.get_credentials()
        return f'{credentials.host}'
