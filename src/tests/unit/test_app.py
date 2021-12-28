import unittest

from src.app import create_app


class TestApp(unittest.TestCase):

    def test_can_create_app(self):
        """Can create an app."""
        app = create_app()

        self.assertIsNotNone(app)

    def test_redirect_to_application_context(self):
        """App has an application context."""
        app = create_app()
        client = app.test_client()

        response = client.get('/')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.location, app.config['APPLICATION_CONTEXT'])
