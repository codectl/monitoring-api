import os

from flasgger import Swagger
from flask import Blueprint, Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from src.cli.test import test_command
from src.settings.config import config_by_name


# SQLite database
db = SQLAlchemy()

# initialize Flask Restful
api = Api()

# initialize swagger
swagger = Swagger()


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

    # initialize root blueprint
    api_bp = Blueprint('api', __name__, url_prefix=app.config['APPLICATION_CONTEXT'])

    # register api blueprint
    app.register_blueprint(api_bp)

    # register cli commands
    app.cli.add_command(test_command)

