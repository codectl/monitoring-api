from flask import Blueprint, jsonify
from flask_restful import abort, Api, Resource

from src.api.bright import BrightAPI
from src.schemas.serlializers.bright import HealthCheckSchema

blueprint = Blueprint("health-checks", __name__)
api = Api(blueprint)


@api.resource("/health-checks", endpoint="health-checks")
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


@api.resource("/health-checks/<key>", endpoint="health-check")
class HealthCheck(Resource):
    def get(self, key):
        """
        Get health check given its identifier.
        ---
        parameters:
            - in: path
              name: key
              schema:
                type: string
              required: true
              description: health check unique identifier
        tags:
            - health-checks
        responses:
            200:
                description: Ok
                content:
                    application/json:
                        schema: HealthCheckSchema
            404:
                $ref: '#/components/responses/NotFound'
        """
        if key not in BrightAPI().supported_measurables():
            abort(404, code=404, reason="Not Found")
        health_check = BrightAPI(verify=False).health_check(key=key)
        return HealthCheckSchema().dump(health_check)


@api.resource("/health-checks/supported-measurables", endpoint="supported-measurables")
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
