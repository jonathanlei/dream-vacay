""" Scraping kayak.com for flight information.
    Returns an instance of flights_list """

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import re
from time import sleep
from random import randint
from models import Flights_List, Flight, RoundTripFlights

# hardcoded search query parameters
# TODO: update with user data later
adults = 1
airport_origin = "SFO"
airport_destination = "JFK"
outbound_date = "2021-01-07"  # YYYY-MM-DD
inbound_date = "2021-01-14"  # YYYY-MM-DD

# Changed airport origin / destination to actual city names to reflect form inputs on explore page
test_dict = {"adults": 1,
             "airport_origin": "San Francisco, United States",
             "airport_destination": "New York City, United States",
             "outbound_date": "2021-01-07",
             "inbound_date": "2021-01-14",
            }   
            #  "airport_origin_code": None,
            #  "airport_destination_code": None
            

# default params in query string for each search
QUERY_PARAM_INPUTS = {
   "sort": "bestflight_a"
}

KAYAK_URL = "https://www.kayak.com/flights/"


# URL info subject to change based on user input later
FLIGHTS_INFO_URL = f'{KAYAK_URL}/{airport_origin}-{airport_destination}/{outbound_date}/{inbound_date}/{adults}adults'


def get_round_trip_flight_info(flight_ticket_container):
    """ Given a flight info container, scrape individual sections and return a flight info instance """

    def get_single_flight_info(flight_container):
        flight_info = {}
        flight_info['airlines'] = {}

        flight_info['airlines']["airline_logo"] = (
            flight_container.findChild("div", {"class": "leg-carrier"})
            .findChild("img")['src'])

        flight_info['airlines']["name"] = (
            flight_container.findChild("div", {"class":"section times"})
            .findChild("div", {"class":"bottom"})
            .text.strip())
        # info string is the arialabel like below
        # "Depart Leg: American Airlines, SFO 11:28 pm - JFK 3:17 pm. Select to show all results with this leg"
        info_string = flight_container.findChild("input", {"name":"specleg"})['aria-label']
        origin_idx = info_string.index(",")
        flight_info["airport_origin"] = info_string[origin_idx+2:origin_idx+5]

        depart_time_idx = origin_idx+6
        divider_idx = info_string.index("-")
        flight_info["takeoff_time"] = info_string[depart_time_idx:divider_idx-1]

        destination_idx = divider_idx+2
        flight_info["airport_destination"] = info_string[destination_idx:destination_idx+3]

        landing_time_idx = destination_idx+4
        period_idx = info_string.index(".")
        flight_info["landing_time"] = info_string[landing_time_idx:period_idx]

        connections = flight_container.findChild("div",{"class": "section stops"}).text.strip().split("\n\n\n")
        flight_info["connections"] = connections[1:]

        flight_info["duration"] = flight_container.findChild("div", {"class": re.compile("section duration")}).findChild("div", {"class":"top"}).text.strip()


        return Flight.fromdict(flight_info)

    total_price = flight_ticket_container.findChild("span", {"class":"price-text"}).text.strip()
    origin_flight_container = flight_ticket_container.findChild("li", {"class": "flight with-gutter"})
    return_flight_container = flight_ticket_container.findChildren("li", {"class": "flight"})[-1]
    origin_flight = get_single_flight_info(origin_flight_container)
    return_flight = get_single_flight_info(return_flight_container)

    statuses = []
    cheapest = flight_ticket_container.findChild("div", {"class": "bf-cheapest"})
    best = flight_ticket_container.findChild("div", {"class": "bf-best"})
    if cheapest:
        statuses.append("cheapest")
    if best:
        statuses.append("best")
    return RoundTripFlights(total_price=total_price,
                            origin_flight=origin_flight,
                            return_flight=return_flight,
                            statuses=statuses)





def get_flights_list_info(search_inputs):
    """ Given a kayak.com flights info url, scrape page and 
    return a list of flight info """

    # First populate the correct airport codes (using Selenium to validate airport codes from user city inputs)
    # but may refactor to use database later to map cities to airports?
    get_city_codes_from(search_inputs)

    # req = requests.get(url=FLIGHTS_INFO_URL, params=search_inputs)
    # soup = BeautifulSoup(req.content, 'html.parser')
    FLIGHTS_INFO_URL = f"""{KAYAK_URL}/{search_inputs['origin_airport_code']}-{search_inputs['destination_airport_code']}/
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
        wait = WebDriverWait(driver, 1800)
        wait.until_not(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "col-advice"), "Loading...")
        )
    finally:
        html = driver.page_source
        driver.quit()

    soup = BeautifulSoup(html, features="html.parser")

    flights_list = Flights_List.fromdict(search_inputs)
    flight_ticket_containers = soup.find_all("div", { 
                                "class": "resultInner"
                                })
    
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

    for ticket_container in filter_quality_flights(flight_ticket_containers):
        flights_list.add_flight(get_round_trip_flight_info(ticket_container))

    return flights_list

        

def get_city_codes_from(search_input):
    """ Gets the city codes from user input for cities on explore page  
    Got help from medium post regarding selecting the correct element to change input text
    https://medium.com/analytics-vidhya/what-if-selenium-could-do-a-better-job-than-your-travel-agency-5e4e74de08b0
    """

    driver = webdriver.Chrome(executable_path='./chromedriver')

    # Sleeping for randint seconds so Kayak doesn't trigger recapcha
    driver.get(KAYAK_URL)
    sleep(randint(2, 5))

    # Origin click path
    origin_click_path = "//*[contains(@id, 'origin-airport-display')]"
    driver.find_element_by_xpath(origin_click_path).click()

    # Origin input box
    origin_text_path = "//input[contains(@id, 'origin-airport')]"
    driver.find_element_by_xpath(origin_text_path).send_keys(Keys.BACKSPACE + Keys.BACKSPACE + search_input["airport_origin"])
    sleep(randint(1, 2))
    driver.find_element_by_xpath(origin_text_path).send_keys(Keys.RETURN)

    sleep(randint(1, 2))

    # Destination click path
    destination_click_path = "//*[contains(@id, 'destination-airport-display')]"
    driver.find_element_by_xpath(destination_click_path).click()
    
    # Destination input box
    destination_text_path = "//input[contains(@id, 'destination-airport')]"
    driver.find_element_by_xpath(destination_text_path).send_keys(Keys.BACKSPACE + Keys.BACKSPACE + search_input["airport_destination"])
    sleep(randint(1, 2))
    driver.find_element_by_xpath(destination_text_path).send_keys(Keys.RETURN)

    search_input["origin_airport_code"] = driver.find_element_by_xpath(origin_click_path).text[-4:-1]
    search_input["destination_airport_code"] = driver.find_element_by_xpath(destination_click_path).text[-4:-1]

    driver.quit()




