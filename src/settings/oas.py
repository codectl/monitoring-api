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
