from werkzeug.exceptions import HTTPException

from flask import redirect, url_for

from src import utils


def ctx_settings(app):

    # redirect root path to context root
    app.add_url_rule("/", "index", view_func=lambda: redirect(url_for("swagger.ui")))

    @app.errorhandler(HTTPException)
    def handle_http_errors(ex):
        """Jsonify http errors."""
        return utils.http_response(ex.code, exclude=("message",)), ex.code
