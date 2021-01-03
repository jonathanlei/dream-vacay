""" Scraping kayak.com for flight information.
    Returns an instance of flights_list """

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from time import sleep
from random import randint
from models import Flights_List, Flight

# hardcoded search query parameters
# TODO: update with user data later
adults = 1
airport_origin = "SFO"
airport_destination = "JFK"
outbound_date = "2021-01-07"  # YYYY-MM-DD
inbound_date = "2021-01-14"  # YYYY-MM-DD

test_dict = {"adults": 1,
             "airport_origin": "SFO",
             "airport_destination": "JFK",
             "outbound_date": "2021-01-07",
             "inbound_date": "2021-01-14"}

# default params in query string for each search
QUERY_PARAM_INPUTS = {
   "sort": "bestflight_a"
}

KAYAK_URL = "https://www.kayak.com/flights/"


# URL info subject to change based on user input later
FLIGHTS_INFO_URL = f'{KAYAK_URL}/{airport_origin}-{airport_destination}/{outbound_date}/{inbound_date}/{adults}adults'


def get_single_flight_info(flight_ticket_container):
    """ Given a flight info container, scrape individual sections and return a flight info instance """
    flight_info = {}
    



def get_flights_list_info(search_inputs):
    """ Given a kayak.com flights info url, scrape page and 
    return a list of flight info """

    # req = requests.get(url=FLIGHTS_INFO_URL, params=search_inputs)
    # soup = BeautifulSoup(req.content, 'html.parser')
    FLIGHTS_INFO_URL = f"""{KAYAK_URL}/{search_inputs['airport_origin']}-{search_inputs['airport_destination']}/
                           {search_inputs['outbound_date']}/{search_inputs['inbound_date']}/{search_inputs['adults']}adults'"""
    # print(req.content)
    driver = webdriver.Chrome(executable_path='./chromedriver')
    sleep(5)

    # Brute forcing a URL here because need to enable JS or else have to use Selenium
    # and you have to provide URL to driver for Selenium
    driver.get(FLIGHTS_INFO_URL)
    sleep(randint(4, 10))
    html = driver.page_source

    soup = BeautifulSoup(html,features="html.parser")

    flights_list = Flights_List.fromdict(search_inputs)
    flight_ticket_containers = soup.find_all("div", { 
                                "class": "resultInner"
                                })
    return flight_ticket_containers
        





