import os
from flask import Flask, Response, json
from migration.controllers import migration
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

app = Flask(__name__)

# Sentry
sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)
sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    integrations=[FlaskIntegration()]
)

# MODULE MIGRATION
app.register_blueprint(migration, url_prefix="/migration")

# Handling 403
@app.errorhandler(403)
def handler_not_found(error):
    data = json.dumps({"message": "Forbidden!"})
    return Response(data, status=403, mimetype="application/json")


# Handling 404
@app.errorhandler(404)
def handler_not_found(error):
    data = json.dumps({"message": "Not found!"})
    return Response(data, status=404, mimetype="application/json")


# Handling 405
@app.errorhandler(405)
def handler_not_found(error):
    data = json.dumps({"message": "Not allowed!"})
    return Response(data, status=405, mimetype="application/json")


# Handling 500
@app.errorhandler(500)
def handler_not_found(error):
    data = json.dumps({"message": "Internal server error!"})
    return Response(data, status=500, mimetype="application/json")


# ENV
debug = os.environ["APP_DEBUG"]
host = os.environ["APP_HOST"]
port = os.environ["APP_PORT"]

# RUN
app.run(debug=debug, host=host, port=port)
