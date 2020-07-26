# [START gae_python37_app]
import datetime
import logging
import socket
from datetime import datetime
from flask import Flask, request
from os import environ

stated = datetime.now().isoformat()


app = Flask(__name__)


@app.route('/')
def index():
    return {
        "ip": request.remote_addr,
        "method": request.method,
        "url": request.url,
        "headers": dict(request.headers),
        "env": dict(environ)
    }

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    (Miracle server)
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    # port = environ.get('PORT')
    # if port:
    #     port = int(port)
    # else:
    #     port = 8080
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
