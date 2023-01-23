from dataclasses import dataclass

from apispec.ext.marshmallow import OpenAPIConverter, resolver

from src.schemas.serializers.http import HttpResponseSchema

__all__ = (
    "create_spec_converter",
    "swagger_configs",
)


def create_spec_converter(openapi_version):
    return OpenAPIConverter(
        openapi_version=openapi_version,
        schema_name_resolver=lambda schema: None,
        spec=None,
    )


def swagger_configs(app_root="/"):
    prefix = "" if app_root == "/" else app_root
    return {
        "url_prefix": prefix,
        "swagger_route": "/",
        "swagger_static": "/static",
        "swagger_favicon": "favicon.ico",
        "swagger_hide_bar": True,
    }
