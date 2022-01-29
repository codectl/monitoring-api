import os

import flasgger
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from webframeworks.
from flask import Blueprint, Flask, redirect, url_for
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_apispec import FlaskApiSpec, doc

from src.cli.test import test_command
from src.settings.config import config_by_name
from src.schemas.serlializers.http import HttpErrorSchema
from src.schemas.serlializers.bright import HealthCheckSchema

# SQLite database
db = SQLAlchemy()

# initialize Flask Restful
api = Api()

docs = FlaskApiSpec(document_options=False)


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

    # initialize root blueprint
    api_bp = Blueprint('api', __name__, url_prefix=app.config['APPLICATION_CONTEXT'])

    # link api to blueprint
    api.init_app(api_bp)

    # register api blueprint
    app.register_blueprint(api_bp)

    # redirect root path to context root
    # app.add_url_rule('/', 'index', lambda: redirect(url_for('flasgger.apidocs')))

    spec = APISpec(
        title=app.config['OPENAPI_SPEC']['info']['title'],
        version=app.config['OPENAPI_SPEC']['info']['version'],
        openapi_version=app.config['OPENAPI_SPEC']['openapi'],
        plugins=(FlaskPlugin(), MarshmallowPlugin()),
        basePath=app.config['APPLICATION_CONTEXT'],
        **app.config['OPENAPI_SPEC']
    )

    from flask_restful import Resource
    # print(app.view_functions)
    # for endpoint, func in app.view_functions:
    #     print(func)
    # spec.path(path=resource[1][0], view=resource[0].as_view())

    # print(api.resources)
    base_path = app.config['APPLICATION_CONTEXT']
    with app.app_context():
        for resource, urls, kwargs in api.resources:
            for url in urls:
                endpoint = kwargs.pop('endpoint')
                # print(url.replace(base_path, ''))
                view = next(v for v in app.view_functions.values() if v.__name__ == endpoint)
                spec.path(path=url.replace(base_path, ''), view=view)

    # # link specs to app
    # docs.init_app(app)
    #
    # # resource discovery
    # docs.register_existing_resources()

    from pprint import pprint
    # pprint(list(app.view_functions.items()))

    # print(api.resources)
    print(spec.to_yaml())

    # print(app.view_functions)
    # spec.path(api)
    # print(docs.spec.to_yaml())

    # register schemas
    # spec.components.schema('HealthCheck', schema=HealthCheckSchema)

    # generate swagger from spec
    swg = flasgger.Swagger(
        app=app,
        config=app.config['SWAGGER'],
        template=flasgger.apispec_to_template(
            app=app,
            spec=spec,
        ),
        merge=True
    )

    with app.app_context():
        import yaml
        print(yaml.dump(swg.get_apispecs('swagger')))

    # print(app.url_map)

    # print('---')
    # with app.app_context():
    #     import pprint
    #     import yaml
    #     print(yaml.dump(swg.get_apispecs('swagger')))

    # register cli commands
    app.cli.add_command(test_command)
