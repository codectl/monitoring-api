import os

import flasgger
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_plugins.webframeworks.flask import FlaskPlugin
from flask import Blueprint, Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from src import __meta__, __version__
from src.cli.test import test_command
from src.resources import health_checks
from src.settings.config import config_by_name
from src.settings.oas import base_template, Server, Tag

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
    url_prefix = app.config['APPLICATION_ROOT']

    # initial blueprint wiring
    index = Blueprint('index', __name__)
    index.register_blueprint(health_checks)
    app.register_blueprint(index, url_prefix=url_prefix)

    # base template for OpenAPI specs
    spec_template = base_template(
        title=__meta__['name'],
        version=__version__,
        openapi_version=app.config['OPENAPI'],
        description=__meta__['summary'],
        servers=[Server(
            url=url_prefix,
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
