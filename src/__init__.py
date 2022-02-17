try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata  # python<=3.7
import src.resources.health_checks

__version__ = metadata.version("monitoring-service")
