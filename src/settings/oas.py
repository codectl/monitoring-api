from dataclasses import dataclass

from apispec.ext.marshmallow import OpenAPIConverter, resolver, SchemaResolver
from apispec.utils import OpenAPIVersion


@dataclass
class Tag:
    name: str
    description: str


@dataclass
class Server:
    url: str
    description: str


@dataclass
class HttpResponse:
    code: str
    reason: str
    description: str


def create_spec_converter(openapi_version):
    return OpenAPIConverter(
        openapi_version=openapi_version,
        schema_name_resolver=lambda schema: None,
        spec=None
    )


def base_template(openapi_version, info={}, servers=(), tags=(), responses=(), schemas=()):
    """Base OpenAPI template."""
    return {
        'openapi': openapi_version,
        'info': {
            'title': kwargs.get('title'),
            'description': kwargs.get('description'),
            'version': kwargs.get('version')
        },
        'servers': servers,
        'tags': tags
    }


def swagger_configs(openapi_version, app_root=''):
    prefix = '' if app_root == '/' else app_root
    return {
        'openapi': openapi_version,
        'specs': [
            {
                'endpoint': 'swagger',
                'route': prefix + '/swagger.json',
                'rule_filter': lambda rule: True,
                'model_filter': lambda tag: True
            }
        ],

        # where to find the docs (ensure trailing slash)
        'specs_route': prefix + '/',

        # swagger static files
        'static_url_path': prefix + '/flasgger_static',

        # hide the Swagger top bar
        'hide_top_bar': True
    }
