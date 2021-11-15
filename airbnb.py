""" scraping airbnb result page and return list of dictionaries about result listings
TODO: scrape individual pages for details if user clicks
TODO : seperate scraping that could change and never changes"""
import requests
from bs4 import BeautifulSoup
import re
from models import Lodgings_List, Lodging
import itertools
from lodging_sort import sort_and_filter_lodgings


test_input = {"city_destination": "Houston--TX--United-States",
              "checkin": "2021-01-10",
              "checkout": "2021-01-15",
              "adults": "2"}

AIRBNB_URL = "https://www.airbnb.com/s/"

def get_single_listing_info(itemlist):
    """ given a bs4 object(listing), get infos about a single listing """
    listing_info = {}

    def find_div_section(itemlist):
        """ find the first div that contains childs, the listing div"""
        divs = itemlist.findChildren("div", {'class': re.compile("^_")})
        for div in divs:
            if len(div.findChildren()) > 1:
                return div

    div_section = find_div_section(itemlist)
    # img_url
    listing_info["img_url"] = div_section.findChild("img")["src"]
    # rating
    try:
        listing_info["rating"] = (div_section.findChild("span", string=re.compile("^Rating"))
                                  .getText()[7:10])
        listing_info["num_ratings"] = div_section.findChild("span", string=re.compile("reviews")).text
    except AttributeError:
        # no rating, add as None
        listing_info["rating"] = None
        listing_info["num_ratings"] = 0
    # total price
    total_text_button = div_section.findChildren("button")[-1].text
    total_text =  total_text_button if total_text_button else div_section.findChildren("span")[-1].text
    total_index = total_text.index("total")
    listing_info["total_price"] = total_text[:total_index-1].replace(u"\xa0", "")

    # room type
    listing_info["room_type"] = div_section.findChild("div", string=re.compile(" in ")).text

    # description
    listing_info["description"] = div_section.findChild("img")["alt"]

    listing_info["lodging_type"] = "Airbnb"

    return Lodging.fromdict(listing_info)


def get_listings_info(search_input):
    """ given a airbnb url, scrape the page and return a list of listings div"""
    # add default params to the inputs
    search_input["source"] = "structured_search_input_header"
    search_input["search_type"] = "unknown"
    search_input["tab_id"] = "home_tab"
    search_input["location"] = search_input["city_destination"]
    # search_input.pop("city_destination")

    r = requests.get(url=AIRBNB_URL, params=search_input)
    soup = BeautifulSoup(r.content, 'html.parser')
    itemlist = soup.find_all(itemprop="itemListElement")
    breakpoint()

    lodgings_list = Lodgings_List.fromdict(search_input)

    for listing in itemlist:
        lodgings_list.add_lodging(get_single_listing_info(listing))
    lodgings_list.lodgings = sort_and_filter_lodgings(lodgings_list.lodgings)
    return lodgings_list
