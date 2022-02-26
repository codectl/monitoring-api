from importlib import metadata

__meta__ = metadata.metadata("monitoring-service")
__version__ = __meta__["version"]
