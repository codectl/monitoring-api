import pytest

from src.app import create_app


@pytest.fixture(scope='session')
def app():
    return create_app(config_name='testing')


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def ctx(app):
    return app.config['APPLICATION_CONTEXT']


class TestApp:

    def test_can_create_app(self, app):
        """Can create an app."""
        assert app is not None

    def test_redirect_root_to_application_context(self, client, ctx):
        """App has an application context."""
        response = client.get('/')
        assert response.status_code == 302

        response = client.get('/', follow_redirects=True)
        request = response.request
        assert response.status_code == 200
        assert request.path.rstrip('/') == ctx

    def test_swagger_apidocs(self, client, ctx):
        """App provides swagger specs."""
        response = client.get(f"{ctx}/swagger.json")

        assert response.status_code == 200
