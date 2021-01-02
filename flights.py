""" Scraping skyscanner.com for flight information.
    Returns an instance of flights_list """

import requests
from bs4 import BeautifulSoup
import re
from models import Flights_List, Flight

# hardcoded search query parameters
# TODO: update with user data later
adults = 2
airport_origin = "SFO"
airport_destination = "JFK"
outbound_date = "210107"  # YYMMDD
inbound_date = "210114"  # YYMMDD

# default params in query string for each search
QUERY_PARAM_INPUTS["adults"] = adults
QUERY_PARAM_INPUTS["adultsv2"] = adults
QUERY_PARAM_INPUTS["children"] = "0"
QUERY_PARAM_INPUTS["childrenv2"] = ""
QUERY_PARAM_INPUTS["inboundaltsenabled"] = "false"
QUERY_PARAM_INPUTS["infants"] = "0"
QUERY_PARAM_INPUTS["outboundaltsenabled"] = "false"
QUERY_PARAM_INPUTS["preferdirects"] = "false"
QUERY_PARAM_INPUTS["preferflexible"] = "false"
QUERY_PARAM_INPUTS["ref"] = "home"
QUERY_PARAM_INPUTS["rtn"] = "1"

SKYSCANNER_URL = "https://www.skyscanner.com/transport/flights/"

request_URL = f'{SKYSCANNER_URL}/{airport_origin}/{airport_destination}/{outbound_date}/{inbound_date'

