import json
import unittest
from unittest.mock import Mock, patch

from src.app import create_app


class TestHealthCheckAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.ctx = self.app.config['APPLICATION_CONTEXT']

        # self.bright = Bright(version='latest')
        # bright.health_checks()

    def tearDown(self):
        pass

    # def test_get_health_checks(self):
    #     """GET request to retrieve a list of health checks."""
    #     response = self.client.get('/health-checks')
    #
    #     self.assertEqual(response.status_code, 200)

    @patch('bright')
    def test_get_no_health_checks(self, mock_bright):
        """GET request to retrieve health checks."""
        mock_bright.health_checks.return_value = []

        response = self.client.get(f"{self.ctx}/health-checks")
        content = json.loads(response.json)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(content, [])

    @patch('bright')
    def test_get_some_health_checks(self, mock_bright):
        """GET request to retrieve health checks."""
        mock_bright.health_checks.return_value = [1, 2, 3]

        response = self.client.get(f"{self.ctx}/health-checks")
        content = json.loads(response.json)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(content, [1, 2, 3])

    def test_get_health_check_by_id(self):
        """GET request to retrieve an health check by id."""
        pass

    def test_get_missing_health_check(self):
        """GET request that cannot retrieve an health check by id."""
        pass
