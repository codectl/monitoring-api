import unittest

from src.app import create_app


class TestApp(unittest.TestCase):

    def setUp(self):
        # create app for testing
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        # self.bright = Bright(version='latest')
        # bright.health_checks()

    def tearDown(self):
        pass

    def test_can_create_app(self):
        """Can create an app."""
        self.assertIsNotNone(self.app)

    def test_redirect_to_application_context(self):
        """App has an application context."""
        app = create_app()
        client = app.test_client()

        response = client.get('/')

        print(1)
        print(response.location)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.location, app.config['APPLICATION_CONTEXT'])
