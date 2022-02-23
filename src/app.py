import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_plugins.webframeworks.flask import FlaskPlugin
from flasgger import apispec_to_template, Swagger
from flask import Blueprint, Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from src import __meta__, __version__
from src.cli.test import test_command
from src.resources.health_checks import blueprint as health_checks
from src.settings import oas
from src.settings.env import config_class, load_dotenv

# SQLite database
db = SQLAlchemy()


def create_app(config_name='development', dotenv=True, configs={}):
    """Create a new app."""

    # define the WSGI application object
    app = Flask(__name__, static_folder=None)

    # load object-based default configuration
    load_dotenv(dotenv)
    app.config.from_object(config_class(config_name))
    app.config.update(configs)

    setup_app(app)

    return app


def setup_app(app):
    """Initial setups."""
    url_prefix = app.config['APPLICATION_ROOT']
    openapi_version = app.config['OPENAPI']

    # initial blueprint wiring
    index = Blueprint('index', __name__)
    index.register_blueprint(health_checks)
    app.register_blueprint(index, url_prefix=url_prefix)

    # base template for OpenAPI specs
    oas.converter = oas.create_spec_converter(openapi_version)
    spec_template = oas.base_template(
        openapi_version=openapi_version,
        info=dict(
            title=__meta__['name'],
            version=__version__,
            description=__meta__['summary']
        ),
        servers=[oas.Server(
            url=url_prefix,
            description=app.config['ENV']
        )],
        tags=[oas.Tag(
            name='health-checks',
            description='All operations involving health-checks',
        )],
        responses=[oas.HttpResponse(
            code=404,
            reason='NotFound',
            description='Not Found'
        )],
        schemas=[HttpResponseSchema]
    )

    spec = APISpec(
        title=__meta__['name'],
        version=__version__,
        openapi_version=openapi_version,
        plugins=(FlaskPlugin(), MarshmallowPlugin()),
        basePath=url_prefix,
        **spec_template
    )

    # create paths from app views
    for view in app.view_functions.values():
        spec.path(
            view=view,
            app=app,
            base_path=url_prefix
        )

    # generate swagger from spec
    Swagger(
        app=app,
        config=oas.swagger_configs(
            openapi_version=openapi_version,
            app_root=url_prefix
        ),
        template=apispec_to_template(
            app=app,
            spec=spec
        ),
        merge=True
    )

    # redirect root path to context root
    app.add_url_rule('/', 'index', view_func=lambda: redirect(url_for('flasgger.apidocs')))

    # register cli commands
    app.cli.add_command(test_command)
