import os
import tempfile
import pytest
from sqlalchemy import create_engine
from tsapp import create_app

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_ECHO': True,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_path,
        'SERVER_NAME': 'localhost'
    })

    with app.app_context():
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        raw_connection = engine.raw_connection()
        raw_connection.executescript(_data_sql)

    yield app

    os.unlink(db_path)


@pytest.fixture
def client(app):
    client = app.test_client()

    context = app.app_context()
    context.push()

    yield client

    context.pop()
