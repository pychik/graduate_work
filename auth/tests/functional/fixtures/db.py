import pytest
from settings.database import db, init_db
from settings.main import app


@pytest.fixture(scope='session', autouse=True)
def test_db():
    init_db(app)
    db.drop_all()
    db.create_all()
    return db
