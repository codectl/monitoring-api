from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_plugins.types import Server, Tag
from apispec_plugins.utils import base_template
from apispec_plugins.webframeworks.flask import FlaskPlugin
from apispec_ui.flask import Swagger
from flask import Blueprint, Flask

from src import __meta__, __version__
from src.api.health_checks import blueprint as health_checks
from src.settings import oas
from src.settings.ctx import ctx_settings
from src.settings.env import config_class, load_dotenv


def create_app(config_name="development", dotenv=True, configs=None):
    """Create a new app."""

    # define the WSGI application object
    app = Flask(__name__, static_folder=None)

    # load object-based default configuration
    load_dotenv(dotenv)
    app.config.from_object(config_class(config_name))
    app.config.update(configs or {})

    setup_app(app)

    return app


def setup_app(app):
    """Initial setups."""
    url_prefix = app.config["APPLICATION_ROOT"]
    openapi_version = app.config["OPENAPI"]

    # initial blueprint wiring
    index = Blueprint("index", __name__)
    index.register_blueprint(health_checks)
    app.register_blueprint(index, url_prefix=url_prefix)

    spec_template = base_template(
        openapi_version=openapi_version,
        info={
            "title": __meta__["name"],
            "version": __version__,
            "description": __meta__["summary"],
        },
        servers=[Server(url=url_prefix, description=app.config["ENV"])],
        tags=[
            Tag(
                name="health-checks",
                description="All operations involving health-checks",
            )
        ],
    )

    spec = APISpec(
        title=__meta__["name"],
        version=__version__,
        openapi_version=openapi_version,
        plugins=(FlaskPlugin(), MarshmallowPlugin()),
        basePath=url_prefix,
        **spec_template
    )

    # create paths from app views
    for view in app.view_functions.values():
        spec.path(view=view, app=app, base_path=url_prefix)

    # create views for Swagger
    Swagger(app=app, apispec=spec, config=oas.swagger_configs(app_root=url_prefix))

    # settings within app ctx
    ctx_settings(app)
