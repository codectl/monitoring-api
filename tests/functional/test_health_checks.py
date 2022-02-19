import pytest
from unittest.mock import MagicMock, Mock

from src.api.bright import BrightAPI
from src.resources import health_checks


@pytest.fixture(scope="function", params=(7, 8))
def bright(request):
    return BrightAPI(
        host='localhost',
        port=80,
        protocol='http',
        basic_auth=('user', 'pass'),
        version=request.param
    )


class TestHealthCheckAPI:

    def test_get_no_health_checks(self, url_prefix, client, bright, mocker):
        """Ensure GET request retrieves health checks."""
        mock = Mock(return_value=bright)
        mock.health_checks.return_value = []
        mocker.patch.object(health_checks, 'BrightAPI', return_value=mock)
        response = client.get(f"{url_prefix}/health-checks")
        assert response.status_code == 200
        assert response.json == []

    # def test_get_some_health_checks(self, client, ctx):
    #     """Ensure GET request retrieves health checks."""
    #     response = client.get(f"{ctx}/health-checks")
    #     content = json.loads(response.json)
    #
    #     assert response.status_code == 200
    #     assert content == [1, 2, 3]
    #
    # def test_get_health_check_by_id(self):
    #     """Ensure GET request retrieves an health check by id."""
    #     pass
    #
    # def test_get_missing_health_check(self):
    #     """Ensure GET request cannot retrieve an health check by id."""
    #     pass
