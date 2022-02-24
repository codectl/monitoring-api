import re

import pytest

from src.api.bright import BrightAPI


@pytest.fixture(scope="class", params=(7, 8))
def bright_http(request):
    return BrightAPI(
        host='localhost',
        port=80,
        protocol='http',
        basic_auth=('user', 'pass'),
        version=request.param
    )


@pytest.fixture(scope="class", params=(7, 8))
def bright_https(request):
    return BrightAPI(
        host='www.localhost',
        port=443,
        protocol='https',
        basic_auth=('user', 'pass'),
        version=request.param
    )


class TestBrightAPI:

    def test_bright_url(self, bright_http, bright_https):
        assert bright_http.url == 'http://localhost:80'
        assert bright_https.url == 'https://www.localhost:443'

    def test_bright_with_basic_auth(self, bright_https):
        assert bright_https._session.auth == ('user', 'pass')

    @pytest.mark.parametrize('version', (7, 8))
    def test_bright_with_cert_auth(self, version):
        bright = BrightAPI(
            host='localhost',
            cert_auth=('cert', 'file'),
            version=version
        )
        assert bright._session.cert == ('cert', 'file')

    @pytest.mark.parametrize('version', (7, 8))
    def test_bright_default_version(self, version, requests_mock):
        matcher = re.compile(r"localhost.*")
        requests_mock.register_uri('POST', matcher, json={'cmVersion': version})
        bright = BrightAPI(
            host='localhost',
            cert_auth=('cert', 'file')
        )
        # assert bright.version ==
