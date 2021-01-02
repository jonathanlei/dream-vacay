""" scraping airbnb result page and return list of dictionaries about result listings"""
import requests
from bs4 import BeautifulSoup
import re


url = """https://www.airbnb.com/s/Kerry--Ireland/homes?tab_id=home_tab&refinement_paths%5B%5D=%2F
homes&adults=1&checkin=2021-02-01&checkout=2021-03-01&source=structured_search_input_header
&search_type=AUTOSUGGEST"""


test_url = "https://www.airbnb.com/s/Houston--TX--United-States/homes?checkin=2021-01-01&checkout=2021-01-08&adults=2&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=unknown&tab_id=home_tab&ne_lat=30.325413658688685&ne_lng=-94.9287617480469&sw_lat=27.527699030304657&sw_lng=-96.2416279589844&zoom=8&search_by_map=true"

test_url2 = "https://www.airbnb.com/s/San-Francisco--CA--United-States/homes?adults=2&checkin=2021-01-07&checkout=2021-02-15&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=autocomplete_click&tab_id=home_tab&query=San%20Francisco%2C%20CA%2C%20United%20States&place_id=ChIJIQBpAG2ahYAR_6128GcTUEo"
# PARAMS = {'auth_key': auth_key, 'url': url} 


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


def get_listings_info(url):
    """ given a airbnb url, scrape the page and return a list of listings div"""
    r = requests.get(url=url)

    soup = BeautifulSoup(r.content, 'html.parser')

    itemlist = soup.find_all(itemprop="itemListElement")[:20]

    listings_info = [get_single_listing_info(listing) for listing in itemlist]

    return listings_info
