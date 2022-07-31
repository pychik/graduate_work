import pytest
import requests
from tests.functional.settings import HTTPResponse, TestSetting


@pytest.fixture(scope='session')
async def settings() -> TestSetting:
    return TestSetting()


@pytest.fixture(scope='session')
async def session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture
async def make_request(session, settings):
    async def inner(url: str,
                    method_name: str = 'GET',
                    data: dict = None) -> HTTPResponse:
        data = data or {}
        url = settings.get_api_url(url)
        method_name = method_name.lower()
        method = getattr(session, method_name)
        with method(url, **data) as response:
            return HTTPResponse(
                body=response.json(),
                headers=response.headers,
                status=response.status_code,
            )

    return inner
