from aenum import MultiValueEnum


class HealthCheckStatus(MultiValueEnum):
    ONLINE = 0, 'PASS'
    UNKNOWN = 1, 'UNKNOWN', 'no data'
    OFFLINE = 2, 'FAIL'
    NONE = None


class HealthCheck:

    def __init__(
            self,
            name: str,
            status: HealthCheckStatus = None,
            node: str = None,
            timestamp: int = None,
            seconds_ago: int = None,
            raw: dict = None
    ):
        self.name = name
        self.status = HealthCheckStatus(status)
        self.node = node
        self.seconds_ago = seconds_ago
        self.timestamp = timestamp
        self.raw = raw
