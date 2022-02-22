import re

import pytest
from requests_mock import ANY

from src.api.bright import BrightAPI
from src.resources import health_checks


@pytest.fixture(scope="class", params=(7, 8))
def bright(request):
    return BrightAPI(
        host='localhost',
        port=80,
        protocol='http',
        basic_auth=('user', 'pass'),
        version=request.param
    )


class TestHealthCheckAPI:

    def test_supported_measurables(self, client):
        response = client.get('/health-checks/supported-measurables')
        assert response.status_code == 200
        assert response.json == ['foo']

    def test_get_no_health_checks(self, client, bright, mocker, requests_mock):
        """Ensure GET request retrieves health checks."""
        matcher = re.compile(rf"{bright.url}.*")
        requests_mock.register_uri(ANY, matcher, json={})
        mocker.patch.object(health_checks, 'BrightAPI', return_value=bright)

        response = client.get('/health-checks')
        assert response.status_code == 200
        assert response.json == []

    # def test_get_an_health_check(self, client, bright, mocker, requests_mock):
    #     """Ensure GET request retrieves health checks."""
    #     response = client.get(f"{ctx}/health-checks")
    #     content = json.loads(response.json)
    #
    #     assert response.status_code == 200
    #     assert content == [1, 2, 3]

    # def test_get_health_check_by_id(self):
    #     """Ensure GET request retrieves an health check by id."""
    #     pass
    #
    # def test_get_missing_health_check(self):
    #     """Ensure GET request cannot retrieve an health check by id."""
    #     pass
