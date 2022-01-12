import requests


class BrightBase:
    """Base class for Bright API."""

    default_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    def __init__(
            self,
            host=None,
            session=None,
            basic_auth=None,
            cert_auth=None,
            version=None,
            verify=True
    ):
        """
        :param session: an already existing session session.
        :param basic_auth: a tuple of username and password to use when establishing a session via HTTP BASIC
        authentication.
        :param cert_auth: a tuple of cert and key to use when establishing a session. The pair is used for both
        authentication and encryption.
        """
        self.host = host
        if session is None:
            self._session = requests.Session()
        else:
            self._session = session
        if basic_auth:
            self._create_basic_session(basic_auth)
        elif cert_auth is not None:
            self._create_cert_session(cert_auth)
        self._session.headers.update(self.default_headers)
        self.version = version
        self.verify = verify

    def _create_basic_session(self, basic_auth):
        self._session.auth = basic_auth

    def _create_cert_session(self, cert_auth):
        self._session.cert = cert_auth

    def version(self):
        url = "{0}/{1}".format(self.host, 'json')
        params = {
            'service': 'cmmain',
            'call': 'getVersion',
        }
        response = self._session.post(
            url=url,
            json=params,
            verify=self.verify
        ).json()
        return response.get('cmVersion')

    def entity(self, name):
        url = "{0}/{1}".format(self.host, 'json')
        params = {
            'service': 'cmdevice',
            'call': 'getDevice',
            'arg': name
        }
        return self._session.post(
            url=url,
            json=params,
            verify=self.verify
        ).json() or {}

    def measurable(self, name):
        url = "{0}/{1}".format(self.host, 'json')
        params = {
            'service': 'cmmon',
            'call': 'getHealthcheck',
            'arg': name
        }
        return self._session.post(
            url=url,
            json=params,
            verify=self.verify
        ).json() or {}
