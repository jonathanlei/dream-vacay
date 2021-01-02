import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import csv
from forms import SearchForm



CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///warbler'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

# connect_db(app)


""" routes
"/"
"/topairbnbs"
"/explore"

"/flights"
"budget"
"""

@app.route("/")
def show_home():
    """ show homepage  """
    return render_template("home.html")

@app.route("/explore")
def show_explore():
    """ show explore page """
    with open('static/csvs/places.csv') as f:
        places = [{k: v for k, v in row.items()}
                  for row in csv.DictReader(f, skipinitialspace=True)]
    form = SearchForm()
    return render_template("explore.html", places=places, form=form)