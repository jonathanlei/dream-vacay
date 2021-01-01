import requests
from bs4 import BeautifulSoup
# """
# URL = "http://api.proxiesapi.com"
# auth_key = "60209c48efa989433e3f5c3924734a9c_sr98766_ooPq87" """


url = """https://www.airbnb.com/s/Kerry--Ireland/homes?tab_id=home_tab&refinement_paths%5B%5D=%2F
homes&adults=1&checkin=2021-02-01&checkout=2021-03-01&source=structured_search_input_header
&search_type=AUTOSUGGEST"""

# PARAMS = {'auth_key': auth_key, 'url': url} 

r = requests.get(url=url)

soup = BeautifulSoup(r.content, 'html.parser')
