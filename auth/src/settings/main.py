from api import init_api
from flask import Flask, request
from flask_marshmallow import Marshmallow
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from settings.config import configuration
from settings.database import init_db
from settings.datastore import init_datastore, init_datastore_commands
from settings.inc_rate_limitter import init_rate_limiter
from settings.jwt import init_jwt


app = Flask(__name__)


@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is required')


app.config.from_object(configuration)

init_db(app)
init_datastore(app)
init_datastore_commands(app)
init_api(app)
init_jwt(app)
init_rate_limiter(app)
FlaskInstrumentor().instrument_app(app)

ma = Marshmallow(app)

app.app_context().push()

if __name__ == '__main__':
    app.run(debug=True)
