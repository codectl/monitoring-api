from dataclasses import dataclass

from src.settings.env import env


@dataclass
class BaseConfig:
    """Base configurations."""

    DEBUG = False
    TESTING = False

    # Application root context
    APPLICATION_ROOT = env.str("APPLICATION_ROOT", "/")

    # OpenAPI supported version
    OPENAPI = env("OPENAPI", "3.0.3")

    # Bright Computing properties
    BRIGHT_COMPUTING_HOST = env.str("BRIGHT_COMPUTING_HOST", "localhost")
    BRIGHT_COMPUTING_PORT = env.int("BRIGHT_COMPUTING_PORT", 8080)
    BRIGHT_COMPUTING_CERT_PATH = env.str(
        "BRIGHT_COMPUTING_CERT_PATH", "/etc/ssl/bright/cert.pem"
    )
    BRIGHT_COMPUTING_KEY_PATH = env.str(
        "BRIGHT_COMPUTING_KEY_PATH", "/etc/ssl/bright/cert.key"
    )

    # List of supported measurables
    SUPPORTED_MEASURABLES = env.list("SUPPORTED_MEASURABLES", [])


@dataclass
class ProductionConfig(BaseConfig):
    ENV = "production"
    LOG_LEVEL = "INFO"


@dataclass
class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True
    LOG_LEVEL = "DEBUG"


@dataclass
class TestingConfig(BaseConfig):
    ENV = "testing"
    TESTING = True
    LOG_LEVEL = "DEBUG"
