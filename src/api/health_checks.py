from flask import Blueprint, jsonify
from flask_restful import abort, Api, Resource

from src.services.bright import BrightSvc
from src.schemas.serlializers.bright import HealthCheckSchema

blueprint = Blueprint("health-checks", __name__, url_prefix="health-checks")
api = Api(blueprint)


@api.resource("/", endpoint="health-checks")
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
        data = BrightSvc(verify=False).health_checks()
        return HealthCheckSchema(many=True).dump(data)


@api.resource("/<key>", endpoint="health-check")
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
        if key not in BrightSvc.supported_measurables():
            abort(404, code=404, reason="Not Found")
        data = BrightSvc(verify=False).health_check(key=key)
        return HealthCheckSchema().dump(data)


@api.resource("/supported-measurables", endpoint="supported-measurables")
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
        return jsonify(BrightSvc.supported_measurables())
