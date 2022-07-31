import json

import pytest
import requests
from models import Role, User, UserSessions
from settings.datastore import security
from tests.functional.utils.dataclass import HTTPResponse


@pytest.fixture(scope='session')
async def session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture
async def make_request(session):
    async def inner(url: str,
                    method_name: str = 'GET',
                    headers: dict = {},
                    data: dict = None) -> HTTPResponse:
        data = data or {}
        method_name = method_name.lower()

        headers.update({'Content-Type': 'application/json',
                        'user-agent': 'Python'})
        method = getattr(session, method_name)
        with method(url, headers=headers, data=json.dumps(data)) as response:
            return HTTPResponse(
                body=response.json() if response.text else None,
                headers=response.headers,
                status=response.status_code,
            )

    return inner


@pytest.fixture(scope='function')
async def test_role():
    name = 'admin'
    description = 'rules the world'
    role = Role(name=name, description=description)
    role.save()
    pk = role.pk
    yield role
    role_exists = role.get_by_pk(pk)
    if role_exists:
        role.delete()


@pytest.fixture(scope='function')
async def test_user(test_role):
    email = 'Testuser@test.com'
    password = 'Test_password'

    user = User(email=email, password=password)
    user.add_role(test_role, security)
    yield user
    user_exists = user.get_by_pk(user.pk)
    if user_exists:
        sessions = UserSessions.query.filter_by(user_id=user.pk)
        sessions.delete()
        user.delete()


@pytest.fixture(scope='function')
async def test_another_user(test_role):
    email = 'new_user@test.com'
    password = 'test_password'

    user = User(email=email, password=password)
    user.add_role(test_role, security)
    yield user


@pytest.fixture(scope='function')
async def other_access_token(test_another_user):
    return test_another_user.get_jwt_token().get('access_token')


@pytest.fixture(scope='function')
async def access_token(test_user):
    return test_user.get_jwt_token().get('access_token')


@pytest.fixture(scope='function')
async def refresh_token(test_user):
    return test_user.get_jwt_token().get('refresh_token')
