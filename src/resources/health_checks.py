from flask_restful import Resource

from src.app import api


@api.resource('/health-checks', endpoint='health_checks')
class HealthChecks(Resource):

    def get(self):
        """Get service tickets based on search criteria."""
        pass
