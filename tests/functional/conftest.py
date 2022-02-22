import pytest

from src.app import create_app
from src.settings.oas import swagger_configs


@pytest.fixture(scope='class')
def app():
    app = create_app(config_name='testing', dotenv=False, configs={
        'FLASK_RUN_HOST': 'localhost',
        'FLASK_RUN_PORT': str(5000),
        'APPLICATION_ROOT': '/',
        'SUPPORTED_MEASURABLES': 'foo',
        'OPENAPI': '3.0.3',
        'SWAGGER': swagger_configs(openapi_version='3.0.3', app_root='/')
    })
    with app.test_request_context():
        yield app


@pytest.fixture(scope='class')
def client(app):
    return app.test_client()
