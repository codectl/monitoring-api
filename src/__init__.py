from importlib import metadata

__meta__ = metadata.metadata("monitoring-api")
__version__ = __meta__["version"]
