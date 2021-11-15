import os
import json

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import csv
from forms import SearchForm
from airbnb import get_listings_info
from flights import get_flights_list_info

# 50 most popular travel destinations
with open('static/csvs/places.csv') as f:
    PLACES = [{k: v for k, v in row.items()} 
              for row in csv.DictReader(f, skipinitialspace=True)]

# all world cities over 150,000 people
with open('static/csvs/worldcities.csv') as f:
    WORLDCITIES = []
    for row in csv.DictReader(f, skipinitialspace=True):
        city_country = ""
        for k, v in row.items():
            if k == "name":
                city_country += v
            if k == "country":
                city_country += f", {v}"
        WORLDCITIES.append(city_country)

TRIPS_SEARCH_BASE_URL = "/trips/s"

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
    form = SearchForm()
    return render_template("explore.html",
                           places=PLACES,
                           form=form,
                           worldcities=json.dumps(WORLDCITIES))


@app.route("/trips/s", methods=["POST"])
def trips_search():
    """ takes form data, and redirect to search result page """
    url = construct_search_url(TRIPS_SEARCH_BASE_URL, request.form)
    return redirect(url)


@app.route("/trips/s/<city_origin>/<city_destination>")
def show_trips_result(city_origin, city_destination):
    """ run scriping app and display trips results"""
    search_input = {"city_origin": city_origin,
                    "city_destination": city_destination,
                    "adults": request.args.get("adults"),
                    "checkin": request.args.get("checkin"),
                    "checkout": request.args.get("checkout")}
    # flights_list = get_flights_list_info(search_input)
    lodgings_list = get_listings_info(search_input)
    flights_list = get_flights_list_info(search_input)
    return render_template("results.html", lodgings_list=lodgings_list, flights_list=flights_list)


def construct_search_url(base_url, form):
    origin = form['origin'].replace(", ", "--").replace(" ", "-")
    result_url = base_url + f"/{origin}"    
    result_url += f"/{form['destination']}"
    result_url += f"?checkin={form['checkin']}"
    result_url += f"&checkout={form['checkout']}"
    result_url += f"&adults={form['adults']}"
    return result_url
