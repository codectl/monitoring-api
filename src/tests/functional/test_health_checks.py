import unittest

from src.app import create_app


class TestHealthCheckAPI(unittest.TestCase):

    def setUp(self):
        # create app for testing
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        # self.bright = Bright(version='latest')
        # bright.health_checks()

    def tearDown(self):
        pass

    # def test_get_health_checks(self):
    #     """GET request to retrieve a list of health checks."""
    #     response = self.client.get('/health-checks')
    #
    #     self.assertEqual(response.status_code, 200)

    def test_get_health_check_by_id(self):
        """GET request to retrieve an health check by id."""
        pass

    def test_get_missing_health_check(self):
        """GET request that cannot retrieve an health check by id."""
        pass

