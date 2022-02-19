import pytest

from src.app import create_app


@pytest.fixture(scope='session')
def app():
    app = create_app(config_name='testing')
    app.config.update({
        'FLASK_RUN_HOST': 'localhost',
        'FLASK_RUN_PORT': 5000,
        'SUPPORTED_MEASURABLES': ['foo']
    })
    with app.test_request_context():
        yield app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def url_prefix(app):
    return app.config['APPLICATION_ROOT']
