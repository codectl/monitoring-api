import os

import flasgger
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_plugins.webframeworks.flask import FlaskPlugin
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from src import __meta__, __version__
from src.cli.test import test_command
from src.resources import health_checks
from src.settings.config import config_by_name
from src.settings.oas import oas_template, Server, Tag

# SQLite database
db = SQLAlchemy()


def create_app(config_name='default'):
    """Create a new app."""

    # define the WSGI application object
    app = Flask(__name__, static_folder=None)

    # load object-based default configuration
    env = os.getenv('FLASK_ENV', config_name)
    app.config.from_object(config_by_name[env])

    setup_app(app)

    return app


def setup_app(app):
    """Initial setups."""
    app.register_blueprint(health_checks, url_prefix=app.config['APPLICATION_CONTEXT'])

    # base template for OpenAPI specs
    spec_template = oas_template(
        title=__meta__['name'],
        version=__version__,
        openapi_version=app.config['OPENAPI'],
        description=__meta__['summary'],
        servers=[Server(
            url=app.config['APPLICATION_CONTEXT'],
            description=app.config['ENV']
        )],
        tags=[Tag(
            name='health-checks',
            description='All operations involving health-checks',
        )]
    )

    spec = APISpec(
        title=__meta__['name'],
        version=__version__,
        openapi_version=app.config['OPENAPI'],
        plugins=(FlaskPlugin(), MarshmallowPlugin()),
        basePath=app.config['APPLICATION_CONTEXT'],
        **spec_template
    )

    # create paths from app views
    for view in app.view_functions.values():
        spec.path(
            view=view,
            app=app,
            base_path=app.config['APPLICATION_CONTEXT']
        )

    # generate swagger from spec
    flasgger.Swagger(
        app=app,
        config=app.config['SWAGGER'],
        template=flasgger.apispec_to_template(
            app=app,
            spec=spec,
        ),
        merge=True
    )

    # redirect root path to context root
    app.add_url_rule('/', 'index', view_func=lambda: redirect(url_for('flasgger.apidocs')))

    # register cli commands
    app.cli.add_command(test_command)
