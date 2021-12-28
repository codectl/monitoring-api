from src.settings.env import env


class BaseConfig:
    """Base configurations."""

    DEBUG = False
    TESTING = False

    # Define host & port
    HOST = env.str('FLASK_RUN_HOST', '0.0.0.0')
    PORT = env.int('FLASK_RUN_PORT', 5000)

    # Application root context
    APPLICATION_CONTEXT = env.str('APPLICATION_CONTEXT', '/')


class ProductionConfig(BaseConfig):
    ENV = 'production'
    LOG_LEVEL = 'INFO'


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class TestingConfig(BaseConfig):
    ENV = 'test'
    TESTING = True
    LOG_LEVEL = 'DEBUG'


config_by_name = dict(
    production=ProductionConfig,
    development=DevelopmentConfig,
    testing=TestingConfig
)
