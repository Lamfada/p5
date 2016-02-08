"""
Flask Website Using Leaflet APIs to create a map.

"""

import flask
from flask import render_template
from flask import request
from flask import url_for

import json
import logging

###
# Globals
###
app = flask.Flask(__name__)
schedule = "static/schedule.txt"  # This should be configurable
import CONFIG


import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)


###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    if 'poi' not in flask.session:
        f = open('./poi.txt')
        pts = []
        for line in f:
            if len(line)==0:
                continue
            else:
                parts = line.split(':')
                entry = {}
                entry['name'] = parts[0]
                entry ['lat'] = parts[1]
                entry['lng'] = parts[2].rstrip()
                pts.append(entry)
        flask.session['poi'] = pts
    return flask.render_template('map.html')

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("map")
    return flask.render_template('page_not_found.html'), 404

###############
#
# AJAX request handlers 
#   These return JSON, rather than rendering pages. 
#
###############

@app.route("/_get_poi")
def get_poi():
    """
    Gives the data of the requested point of interest 
    """
    
    f = open('./poi.txt')
    a = ""
    for line in f:
        a += line
    print(a)
    return jsonify(result=a)
             

if __name__ == "__main__":
    # Standalone, with a dynamically generated
    # secret key, accessible outside only if debugging is not on
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    if app.debug: 
        print("Accessible only on localhost")
        app.run(port=CONFIG.PORT)  # Accessible only on localhost
    else:
        print("Opening for global access on port {}".format(CONFIG.PORT))
        app.run(port=CONFIG.PORT, host="0.0.0.0")
else:
    # Running from cgi-bin or from gunicorn WSGI server, 
    # which makes the call to app.run.  Gunicorn may invoke more than
    # one instance for concurrent service. 
    app.secret_key = CONFIG.secret_key
    app.debug=False

