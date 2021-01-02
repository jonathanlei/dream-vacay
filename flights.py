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

# default params in query string for each search
QUERY_PARAM_INPUTS = {
   "sort": "bestflight_a"
}

KAYAK_URL = "https://www.kayak.com/flights/"

# URL info subject to change based on user input later
FLIGHTS_INFO_URL = f'{KAYAK_URL}/{airport_origin}-{airport_destination}/{outbound_date}/{inbound_date}/{adults}adults'

def get_flights_list_info(search_inputs):
    """ Given a kayak.com flights info url, scrape page and 
    return a list of flight info """

    # req = requests.get(url=FLIGHTS_INFO_URL, params=search_inputs)
    # soup = BeautifulSoup(req.content, 'html.parser')

    # print(req.content)

    driver = webdriver.Chrome(executable_path='./chromedriver')
    # Brute forcing a URL here because need to enable JS or else have to use Selenium
    # and you have to provide URL to driver for Selenium
    driver.get("https://www.kayak.com/flights/LAX-SFO/2021-01-31/2021-02-07?sort=bestflight_a")
    sleep(randint(4,10))
    html = driver.page_source

    soup = BeautifulSoup(html)

    flight_ticket_containers = soup.find_all("div", { 
                                "class": "resultInner"
                                })
   
    return flight_ticket_containers
        

flight_ticket_containers = get_flights_list_info(QUERY_PARAM_INPUTS)


