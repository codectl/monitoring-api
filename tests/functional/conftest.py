import pytest

from src.app import create_app


@pytest.fixture(scope='module')
def app():
    app = create_app(config_name='testing', configs={
        'FLASK_RUN_HOST': 'localhost',
        'FLASK_RUN_PORT': str(5000),
        'APPLICATION_ROOT': '/',
        'SUPPORTED_MEASURABLES': 'foo'
    })
    with app.test_request_context():
        yield app


@pytest.fixture(scope='module')
def client(app):
    return app.test_client()
