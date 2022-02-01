import marshmallow
from flasgger.marshmallow_apispec import schema2parameters
from flask import jsonify
from flask_restful import Resource
from apispec_plugins.utils import spec_from

from src.app import api
from src.api.bright import BrightAPI
from src.schemas.serlializers.bright import HealthCheckSchema


@api.resource('/health-checks', endpoint='health-checks')
class HealthChecks(Resource):

    def get(self):
        """
        Get available health checks.
        ---
        tags:
            - health-checks
        responses:
            200:
                description: Ok
                content:
                    application/json:
                        schema:
                            type: array
                            items: HealthCheckSchema
        """
        health_checks = BrightAPI(verify=False).health_checks()
        return HealthCheckSchema(many=True).dump(health_checks)


@api.resource('/health-check/<key>', endpoint='health-check')
class HealthCheck(Resource):

    @spec_from({
        'parameters': schema2parameters(
            marshmallow.Schema.from_dict({
                'key': marshmallow.fields.String(
                    required=True,
                    metadata=dict(description='ticket unique identifier')
                )
            }),
            location='path'
        ),
        'tags': ['health-checks'],
        'responses': {
            200: {
                'description': 'Ok',
                'content': {
                    'application/json': {
                        'schema': 'HealthCheckSchema'
                    }
                }
            }
        }
    })
    def get(self, key):
        """
        Get health check given its identifier.
        """
        health_check = BrightAPI(verify=False).health_check(key=key)
        return HealthCheckSchema().dump(health_check)


@api.resource('/health-checks/supported-measurables', endpoint='supported-measurables')
class SupportedMeasurables(Resource):

    def get(self):
        """
        Lists currently supported health check measurables.
        ---
        tags:
            - health-checks
        responses:
            200:
                description: Ok
                content:
                    application/json:
                        schema:
                            type: array
                            items: HealthCheckSchema
        """
        return jsonify(BrightAPI.supported_measurables())

