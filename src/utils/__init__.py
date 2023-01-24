from apispec_plugins.types import HTTPResponse
from flask_restful import abort
from werkzeug.http import HTTP_STATUS_CODES

from src.schemas.serializers.http import HttpResponseSchema


def http_response(code: int, description="", **kwargs):
    reason = HTTP_STATUS_CODES[code]
    description = f"{reason}: {description}" if description else reason
    response = HTTPResponse(code=code, description=description)
    return HttpResponseSchema(**kwargs).dump(response)


def abort_with(code: int, description="", **kwargs):
    abort(code, **http_response(code, description=description, **kwargs))
