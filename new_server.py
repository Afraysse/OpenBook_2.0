"""Openbook - A Writing Database"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, flash, redirect, session, request, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Draft, Published


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "CBA"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

########################################################################

@app.route('/')
def index():
    """Homepage"""

    return render_template("homepage.html")

@app.route('')