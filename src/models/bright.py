from aenum import MultiValueEnum


class HealthCheckStatus(MultiValueEnum):
    ONLINE = 0, 'PASS'
    UNKNOWN = 1, 'UNKNOWN', 'no data'
    OFFLINE = 2, 'FAIL'
    NONE = None


class HealthCheck:

    def __init__(
            self,
            status=None
    ):
        self.status = HealthCheckStatus(status)
