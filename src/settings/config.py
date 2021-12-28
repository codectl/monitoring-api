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

    # Swagger properties
    OPENAPI = env('OPENAPI', '3.0.3')
    SWAGGER = {
        'openapi': OPENAPI,
        'specs': [
            {
                'endpoint': 'swagger',
                'route': APPLICATION_CONTEXT + '/swagger.json',
                'rule_filter': lambda rule: True,
                'model_filter': lambda tag: True
            }
        ],

        # where to find the docs (ensure trailing slash)
        'specs_route': APPLICATION_CONTEXT + '/',

        # swagger static files
        'static_url_path': APPLICATION_CONTEXT + '/flasgger_static',

        # hide the Swagger top bar
        'hide_top_bar': True
    }


class ProductionConfig(BaseConfig):
    ENV = 'production'
    LOG_LEVEL = 'INFO'


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class TestingConfig(BaseConfig):
    ENV = 'testing'
    TESTING = True
    LOG_LEVEL = 'DEBUG'


config_by_name = dict(
    production=ProductionConfig,
    development=DevelopmentConfig,
    testing=TestingConfig
)
