import os

from flask import Flask

from src.cli.test import test_command
from src.settings.config import config_by_name


def create_app(config_name='default'):
    """Create a new app."""

    # define the WSGI application object
    app = Flask(__name__)

    # load object-based default configuration
    env = os.getenv('FLASK_ENV', config_name)
    app.config.from_object(config_by_name[env])

    setup_app(app)

    return app


def setup_app(app):

    # register cli commands
    app.cli.add_command(test_command)
