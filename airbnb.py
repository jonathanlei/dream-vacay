""" scraping airbnb result page and return list of dictionaries about result listings"""
import requests
from bs4 import BeautifulSoup
import re
from models import Lodgings_List, Lodging


test_input = {"location": "Houston--TX--United-States",
              "checkin": "2021-01-02",
              "checkout": "2021-01-08",
              "adults": "2"}

AIRBNB_URL = "https://www.airbnb.com/s"


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
    except AttributeError:
        # no rating, add as None
        listing_info["rating"] = None
    # total price
    total_text = div_section.findChildren("button")[-1].text
    total_index = total_text.index("total")
    listing_info["total"] = total_text[:total_index+5].replace(u"\xa0", "")

    # room type
    listing_info["room_type"] = div_section.findChild("div", string=re.compile(" in ")).text

    # description
    listing_info["description"] = div_section.findChild("img")["alt"]

    return listing_info


def get_listings_info(search_input):
    """ given a airbnb url, scrape the page and return a list of listings div"""
    # add default params to the inputs
    test_input["source"] = "structured_search_input_header"
    test_input["search_type"] = "unknown"
    test_input["tab_id"] = "home_tab"

    r = requests.get(url=AIRBNB_URL, params=search_input)

    soup = BeautifulSoup(r.content, 'html.parser')

    itemlist = soup.find_all(itemprop="itemListElement")

    lodgins_list = Lodgings_List(**search_input)

    listings_info = [get_single_listing_info(listing) for listing in itemlist]

    return listings_info
