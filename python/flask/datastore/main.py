# [START gae_python37_app]
import datetime
import logging
import socket
import time
from datetime import datetime
from flask import Flask, request
from os import environ
from google.cloud import datastore

db = datastore.Client()

app = Flask(__name__)

@app.route('/')
def index():
    visit = datastore.Entity(db.key('visit', int(round(time.time() * 1000))))
    forwarded = request.headers.get('x-forwarded-for')
    if forwarded:
        visit['ip'] = forwarded.split(',')[0].strip()
    else:
        visit['ip'] = request.remote_addr
    location = request.headers.get('x-appengine-citylatlong')
    if location:
        [visit['latitude'], visit['longitude']] = location.split(',')
    city = request.headers.get('x-appengine-city')
    if city:
        visit['city'] = city
        visit['country'] = request.headers.get('x-appengine-country')
    visit['agent'] = request.headers.get('user-agent')
    db.put(visit)
    return visit

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
    port = environ.get('PORT')
    if port:
        port = int(port)
    else:
        port = 8080
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
