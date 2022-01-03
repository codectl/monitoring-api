__version_info__ = (0, 0, 1)
__version__ = '.'.join(str(c) for c in __version_info__)

# dummy imports for api discovery
import src.resources.health_checks
