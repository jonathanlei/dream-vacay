""" Scraping skyscanner.com for flight information.
    Returns an instance of flights_list """

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
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
QUERY_PARAM_INPUTS = {
    "adults" : adults,
    "adultsv2" : adults,
    "children" : "0",
    "childrenv2" : "",
    "inboundaltsenabled" : "false",
    "infants" : "0",
    "outboundaltsenabled" : "false",
    "preferdirects" : "false",
    "preferflexible" : "false",
    "ref" : "home",
    "rtn" : "1",
}


SKYSCANNER_URL = "https://www.skyscanner.com/transport/flights/"

# URL info subject to change based on user input later
FLIGHTS_INFO_URL = f'{SKYSCANNER_URL}/{airport_origin}/{airport_destination}/{outbound_date}/{inbound_date}'

def get_flights_list_info(search_inputs):
    """ Given a skyscanner flights info url, scrape page and 
    return a list of flight info """

    # req = requests.get(url=FLIGHTS_INFO_URL, params=QUERY_PARAM_INPUTS)
    # soup = BeautifulSoup(req.content, 'html.parser')

    driver = webdriver.Chrome(executable_path='./chromedriver')
    # Brute forcing a URL here because need to enable JS or else have to use Selenium
    # and you have to provide URL to driver for Selenium
    # driver.get("https://www.kayak.com/flights/LAX-SFO/2021-01-31/2021-02-07?sort=bestflight_a")
    html = driver.page_source

    soup = BeautifulSoup(html)
    print(soup)

    flight_ticket_containers = soup.find_all("div", { 
                                "class": re.compile("^FlightsTicket_container")
                                })

    print(flight_ticket_containers)
        





