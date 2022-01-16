from flask_restful import Resource

from src.app import api
from src.api.bright import BrightAPI
from src.serialization.serlializers.bright import HealthCheckSchema


@api.resource('/health-checks', endpoint='health_checks')
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
        health_checks = BrightAPI().health_checks()

        return HealthCheckSchema(many=True).dump(health_checks)
