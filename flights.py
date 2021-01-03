""" Scraping kayak.com for flight information.
    Returns an instance of flights_list """

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    breakpoint()




def get_flights_list_info(search_inputs):
    """ Given a kayak.com flights info url, scrape page and 
    return a list of flight info """

    # req = requests.get(url=FLIGHTS_INFO_URL, params=search_inputs)
    # soup = BeautifulSoup(req.content, 'html.parser')
    FLIGHTS_INFO_URL = f"""{KAYAK_URL}/{search_inputs['airport_origin']}-{search_inputs['airport_destination']}/
                           {search_inputs['outbound_date']}/{search_inputs['inbound_date']}/{search_inputs['adults']}adults'"""
    # print(req.content)
    driver = webdriver.Chrome(executable_path='./chromedriver')

    # Brute forcing a URL here because need to enable JS or else have to use Selenium
    # and you have to provide URL to driver for Selenium
    # Sleeping for randint seconds so Kayak doesn't trigger recapcha
    driver.get(FLIGHTS_INFO_URL)
    sleep(randint(4, 10))

    # Waiting until page fully loads, tags for best / cheapest flights are in right places
    # Using the loading indicator for a particular element on site as the bottleneck
    try:
        wait = WebDriverWait(driver, 10)
        wait.until_not(
            EC.text_to_be_present_in_element((By.ID, re.compile("-advice")), "Loading...")
        )
    finally:
        html = driver.page_source
        driver.quit()


    soup = BeautifulSoup(html, features="html.parser")

    flights_list = Flights_List.fromdict(search_inputs)
    flight_ticket_containers = soup.find_all("div", { 
                                "class": "resultInner"
                                })

    for ticket_container in filter_quality_flights(flight_ticket_containers):
        flights_list.add_flight(get_single_flight_info(ticket_container))

    return flights_list

def is_quality_flight(flight_container):
    """ Filter comparator function to check if flight is good. May need to add another 
    tag for eco-friendly later """

    cheapest = flight_container.findChild("div", {"class": "bf-cheapest"})
    best = flight_container.findChild("div", {"class": "bf-best"})
    if cheapest or best:
        return True
    return False


def filter_quality_flights(flight_ticket_containers):
    """ Takes flight infos based on cheapest, best, and eco-friendly tag """

    return list(filter(is_quality_flight, flight_ticket_containers))



        





