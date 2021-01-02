import requests
from bs4 import BeautifulSoup
import re
# """
# URL = "http://api.proxiesapi.com"
# auth_key = "60209c48efa989433e3f5c3924734a9c_sr98766_ooPq87" """


url = """https://www.airbnb.com/s/Kerry--Ireland/homes?tab_id=home_tab&refinement_paths%5B%5D=%2F
homes&adults=1&checkin=2021-02-01&checkout=2021-03-01&source=structured_search_input_header
&search_type=AUTOSUGGEST"""


test_url = "https://www.airbnb.com/s/Paris--France/homes?refinementPaths%5B%5D=%2Fhomes&place_id=ChIJD7fiBh9u5kcRYJSMaMOCCwQ&adults=2&checkin=2021-01-07&checkout=2021-02-15&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=AUTOSUGGEST"

test_url2 = "https://www.airbnb.com/s/San-Francisco--CA--United-States/homes?adults=2&checkin=2021-01-07&checkout=2021-02-15&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=autocomplete_click&tab_id=home_tab&query=San%20Francisco%2C%20CA%2C%20United%20States&place_id=ChIJIQBpAG2ahYAR_6128GcTUEo"
# PARAMS = {'auth_key': auth_key, 'url': url} 

r = requests.get(url=test_url)

soup = BeautifulSoup(r.content, 'html.parser')

itemlist = soup.find(itemprop="itemListElement")
# finding the div section


def find_div_section(itemlist):
    divs = itemlist.findChildren("div", {'class': re.compile("^_")})
    for div in divs:
        if len(div.findChildren()) > 0:
            return div


div_section = find_div_section(itemlist)
# img_url
img_url = div_section.findChild("img")["src"]
# rating
rating_span = div_section.findChild("span", string=re.compile("^Rating")).getText()
rating = rating_span[7:10]

# #price per night 
# price = div_section.findChild("span", string=re.compile("rice")).parent.text
# dollar_index = price.index("$")
# price = price[dollar_index:].replace(u"\xa0", "")

# total price
total_text = div_section.findChildren("button")[-1].text
total_index = total_text.index("total")
total = total_text[:total_index+5].replace(u"\xa0", "")

# room type
room_type = div_section.findChild("div", string=re.compile(" in ")).text

# description
description = div_section.findChild("img")["alt"]
