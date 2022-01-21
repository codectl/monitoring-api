import flasgger
import marshmallow
from flasgger.marshmallow_apispec import schema2parameters
from flask import jsonify
from flask_restful import Resource

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
                            items:
                                $ref: '#/components/schemas/HealthCheck'
        """
        health_checks = BrightAPI(verify=False).health_checks()
        return HealthCheckSchema(many=True).dump(health_checks)


@api.resource('/health-check/<key>', endpoint='health-check')
class HealthCheck(Resource):

    @flasgger.swag_from({
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
                        'schema': {
                            '$ref': '#/components/schemas/HealthCheck'
                        }
                    }
                }
            }
        }
    })
    def get(self, key):
        """Get health check given its identifier."""
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
                            items:
                                type: string
        """
        return jsonify(BrightAPI.supported_measurables())
