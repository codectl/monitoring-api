from aenum import MultiValueEnum
from dataclasses import dataclass


class HealthCheckStatus(MultiValueEnum):
    ONLINE = 0, "PASS"
    UNKNOWN = 1, "UNKNOWN", "no data"
    OFFLINE = 2, "FAIL"
    NONE = None


@dataclass
class HealthCheck:
    name: str
    status: HealthCheckStatus = HealthCheckStatus.NONE
    node: str = None
    timestamp: int = None
    seconds_ago: int = None
    raw: dict = None
