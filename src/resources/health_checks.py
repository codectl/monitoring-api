import flasgger
from flask_restful import Resource

from src.app import api
from src.api.bright import Bright


@api.resource('/health-checks', endpoint='health_checks')
class HealthChecks(Resource):

    @flasgger.swag_from({
        'tags': ['health-checks'],
        'responses': {
            200: {
                'description': 'Ok',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'array',
                            'items': {
                                '$ref': '#/components/schemas/Issue'
                            }
                        }
                    },
                }
            }
        },
    })
    def get(self):
        """Get available health checks."""

        pass
