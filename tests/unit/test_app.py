import unittest

from src.app import create_app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.ctx = self.app.config['APPLICATION_CONTEXT']

    def tearDown(self):
        pass

    def test_can_create_app(self):
        """Can create an app."""
        self.assertIsNotNone(self.app)

    def test_redirect_root_to_application_context(self):
        """App has an application context."""
        response = self.client.get('/')
        self.assertEquals(response.status_code, 302)

        response = self.client.get('/', follow_redirects=True)
        request = response.request
        self.assertEquals(response.status_code, 200)
        self.assertEquals(request.path.rstrip('/'), self.ctx)

    def test_swagger_apidocs(self):
        """App provides swagger specs."""
        response = self.client.get(f"{self.ctx}/swagger.json")

        self.assertEquals(response.status_code, 200)
