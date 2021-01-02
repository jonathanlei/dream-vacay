""" Requests for flight information """

import requests
from secrets import X_RAPIDAPI_KEY

SKYSCANNER_HOST = 'skyscanner-skyscanner-flight-search-v1.p.rapidapi.com'

#TODO: Hardcoding these path terms, user should be able to change with each search later
LOCALE = "en-US"
COUNTRY = "US"
CURRENCY = "USD"
OUTBOUND_DATE = "2021-02-01"
INBOUND_DATE = "2021-03-01"

SKYSCANNER_PLACES_URL = f"https://{SKYSCANNER_HOST}/apiservices/autosuggest/v1.0/{COUNTRY}/{CURRENCY}/{LOCALE}/"
SKYSCANNER_QUOTES_URL = f"https://{SKYSCANNER_HOST}/apiservices/browsequotes/v1.0/{COUNTRY}/{CURRENCY}/{LOCALE}/{OUTBOUND_DATE}"

HEADERS = {
    'x-rapidapi-key': X_RAPIDAPI_KEY,
    'x-rapidapi-host': SKYSCANNER_HOST
    }

QUOTES_QUERY_PARAMS = {
    "inboundpartialdate": INBOUND_DATE
}

# hardcoded a city query
#TODO: update with user data later
ORIGIN = "San Francisco"
DESTINATION = "New York City"

def get_airport_codes(city):
    """ Get all the airport codes for a particular origin or destination city """

    req = requests.get(
        url=SKYSCANNER_PLACES_URL,
        headers=HEADERS,
        params={"query": city}
        )
    places_data = req.json()["Places"]
    airport_codes = [airport["PlaceId"] for airport in places_data]
    return airport_codes


# Do this twice for origin and destination
origin_codes = get_airport_codes(ORIGIN)
destination_codes = get_airport_codes(DESTINATION)

#TODO: update with user selection later
origin = origin_codes[0]  # Selecting SFO airport
destination = destination_codes[1]  # Selecting JFK airport

def get_flight_list(origin, destination):
    """ Get all the flights for a particular origin and destination route """

    req = requests.get(
        url=SKYSCANNER_QUOTES_URL,
        headers=HEADERS,
        params=QUOTES_QUERY_PARAMS
        )
    flights_data = req.json()["Quotes"]
    return flights_data  # this is not what you want
