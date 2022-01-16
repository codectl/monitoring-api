import os

import flasgger
import yaml

from src import __version__
from src.settings.env import env


class BaseConfig:
    """Base configurations."""

    DEBUG = False
    TESTING = False

    ENV = env.str('FLASK_ENV')
    HOST = env.str('FLASK_RUN_HOST', 'localhost')
    PORT = env.int('FLASK_RUN_PORT', 5000)

    # Application root context
    APPLICATION_CONTEXT = env.str('APPLICATION_CONTEXT', '/')

    # Bright Computing properties
    BRIGHT_COMPUTING_HOST = env.str('BRIGHT_COMPUTING_HOST', 'localhost')
    BRIGHT_COMPUTING_PORT = env.int('BRIGHT_COMPUTING_PORT', 8080)
    BRIGHT_COMPUTING_CERT_PATH = env.str('BRIGHT_COMPUTING_CERT_PATH', '/etc/ssl/bright/cert.pem')
    BRIGHT_COMPUTING_KEY_PATH = env.str('BRIGHT_COMPUTING_KEY_PATH', '/etc/ssl/bright/cert.key')

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

    # OpenAPI 3 properties
    OPENAPI_SPEC = yaml.safe_load(flasgger.utils.load_from_file(
        os.path.join('src', 'settings', 'oas3.yaml')
    ).format(**{
        'OPENAPI': OPENAPI,
        'APPLICATION_CONTEXT': APPLICATION_CONTEXT,
        'ENV': ENV,
        'VERSION': __version__
    }))


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
