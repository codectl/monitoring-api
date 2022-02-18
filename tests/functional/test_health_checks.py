import pytest
import json

from src.api.bright import BrightAPI


@pytest.fixture(scope="function", params=(7, 8))
def bright(request):
    return BrightAPI(
        host='localhost',
        port=80,
        protocol='http',
        version=request.param
    )


class TestHealthCheckAPI:

    def test_get_no_health_checks(self, ctx, client, app):
        """Ensure GET request retrieves health checks."""
        response = client.get(f"{ctx}/health-checks")
        print(app.config)
        print(11111111111111111)
        print(response.json)
        # content = json.loads(response.json)
        #
        assert False
        # assert response.status_code == 200
        # assert content == []

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
