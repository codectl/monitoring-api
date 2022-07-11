import re
import time

import pytest

from src.services.bright import BrightAPI
from src.models.bright import HealthCheck, HealthCheckStatus


@pytest.fixture(scope="class", params=(7, 8))
def bright_http(request):
    return BrightAPI(
        host="localhost",
        port=80,
        protocol="http",
        basic_auth=("user", "pass"),
        version=request.param,
    )


@pytest.fixture(scope="class", params=(7, 8))
def bright_https(request):
    return BrightAPI(
        host="www.localhost",
        port=443,
        protocol="https",
        basic_auth=("user", "pass"),
        version=request.param,
    )


class TestBrightAPI:
    def test_bright_url(self, bright_http, bright_https):
        assert bright_http.url == "http://localhost:80"
        assert bright_https.url == "https://www.localhost:443"

    def test_bright_with_basic_auth(self, bright_https):
        assert bright_https._session.auth == ("user", "pass")

    @pytest.mark.parametrize("version", (7, 8))
    def test_bright_with_cert_auth(self, version):
        bright = BrightAPI(
            host="localhost", cert_auth=("cert", "file"), version=version
        )
        assert bright._session.cert == ("cert", "file")

    @pytest.mark.parametrize("version", (7, 8, 7.2, 8.2, "7.2", "8.2"))
    def test_bright_default_version(self, version, requests_mock):
        matcher = re.compile(r"localhost.*")
        requests_mock.register_uri("POST", matcher, json={"cmVersion": version})
        bright = BrightAPI(host="localhost", cert_auth=("cert", "file"))
        major_version = int(float(version))
        assert bright.version == version
        assert type(bright.instance).__name__ == f"Bright{major_version}"

    @pytest.mark.parametrize("value", ("PASS", "FAIL", "UNKNOWN"))
    def test_bright8_health_check(self, value, mocker, requests_mock):
        bright = BrightAPI(host="localhost", basic_auth=("user", "pass"), version=8)
        mocker.patch.object(bright, "supported_measurables", return_value=["foo"])
        data = {
            "data": [
                {
                    "age": 0,
                    "entity": "foo_node",
                    "measurable": "foo",
                    "time": 0,
                    "value": value,
                }
            ]
        }
        matcher = re.compile(rf"{bright.url}.*")
        requests_mock.register_uri("GET", matcher, json=data)
        expected = HealthCheck(
            name="foo",
            status=HealthCheckStatus(value),
            node="foo_node",
            timestamp=0,
            seconds_ago=0,
            raw=data["data"][0],
        )

        health_check = bright.health_check("foo")
        assert health_check == expected

    @pytest.mark.parametrize("rate", (0, 0.0, 1, 1.0, 2, 2.0))
    def test_bright7_health_check(self, rate, mocker, requests_mock):
        bright = BrightAPI(host="localhost", basic_auth=("user", "pass"), version=7)
        mocker.patch.object(bright, "supported_measurables", return_value=["foo"])
        mocker.patch.object(
            bright.instance, "measurable", return_value={"uniqueKey": 1}
        )
        mocker.patch.object(bright.instance, "entity", return_value={"uniqueKey": 1})
        mocker.patch.object(time, "time", return_value=0)
        data = [
            {
                "timeStamp": 0,
                "rate": rate,
                "devId": 1,
                "metricId": 1,
                "severity": 1,
                "uniqueKey": 1,
            }
        ]
        matcher = re.compile(rf"{bright.url}.*")
        requests_mock.register_uri("POST", matcher, json=data)
        expected = HealthCheck(
            name="foo",
            status=HealthCheckStatus(rate),
            node="foo_node",
            timestamp=0,
            seconds_ago=0,
            raw={**data[0], "measurable": "foo", "entity": "foo_node"},
        )

        health_check = bright.health_check("foo", node="foo_node")
        assert health_check == expected

    @pytest.mark.parametrize("version", (7, 8))
    def test_unsupported_health_check(self, version, mocker):
        bright = BrightAPI(
            host="localhost", basic_auth=("user", "pass"), version=version
        )
        mocker.patch.object(bright, "supported_measurables", return_value=["foo"])
        assert bright.health_check(key="bar") is None
