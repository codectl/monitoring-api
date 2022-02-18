from dataclasses import dataclass


@dataclass
class Tag:
    name: str
    description: str


@dataclass
class Server:
    url: str
    description: str


def oas_template(openapi_version, servers=(), tags=(), **kwargs):
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


def swagger_configs(openapi_version, app_root):
    return {
        'openapi': openapi_version,
        'specs': [
            {
                'endpoint': 'swagger',
                'route': app_root + '/swagger.json',
                'rule_filter': lambda rule: True,
                'model_filter': lambda tag: True
            }
        ],

        # where to find the docs (ensure trailing slash)
        'specs_route': app_root + '/',

        # swagger static files
        'static_url_path': app_root + '/flasgger_static',

        # hide the Swagger top bar
        'hide_top_bar': True
    }
