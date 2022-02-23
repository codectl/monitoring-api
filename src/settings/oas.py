from dataclasses import dataclass

from apispec.ext.marshmallow import OpenAPIConverter, resolver
from apispec.utils import OpenAPIVersion

from src.schemas.serlializers.http import HttpResponseSchema


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


def base_template(openapi_version, info={}, servers=(), tags=(), responses=()):
    """Base OpenAPI template."""
    return {
        'openapi': openapi_version,
        'info': info,
        'servers': servers,
        'tags': tags,
        'components': {
            'responses': {
                response.reason: {
                    'description': response.description,
                    'content': {
                        'application/json': {
                            'schema': {
                                '$ref': '#/components/schemas/HttpResponse'
                            }
                        }
                    }
                } for response in responses
            },
            'schemas': {
                resolver(HttpResponseSchema): {
                    **converter.schema2jsonschema(schema=HttpResponseSchema)
                }
            } if responses else {}
        }
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
        'static_url_path': prefix + '/static',

        # hide the Swagger top bar
        'hide_top_bar': True
    }
