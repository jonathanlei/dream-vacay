""" get 50 most popular places traveled in the world into a database"""
import requests
from bs4 import BeautifulSoup
import csv


URL = "http://api.proxiesapi.com"
auth_key = "60209c48efa989433e3f5c3924734a9c_sr98766_ooPq87"
FORBES_URL = "https://www.forbes.com/sites/laurabegleybloom/2019/09/04/bucket-list-travel-the-top-50-places-in-the-world/?sh=2b1e34c620cf"
PARAMS = {'auth_key': auth_key, 'url': FORBES_URL}

#get html using beautiful soup
r = requests.get(url=URL, params=PARAMS)
soup = BeautifulSoup(r.content, 'html.parser')

place_list_html = soup.find_all("strong")

# clean up strings
place_list = []
for place in place_list_html:
    for letter in place.get_text().strip():
        if letter.isupper():
            index = int(place.get_text().strip().index(letter))
            # clean up strings and convert them in query string format
            place = place.get_text().strip()[index:]
            place = place.replace(":", "") 
            place = place.replace(u'\xa0', " ")
            place = place.replace(", ", "--")
            place = place.replace(" ", "-")
            place_list.append(place)
            break

UPSPLASH_URL = "https://unsplash.com/s/photos"


def get_image(name):

    url = UPSPLASH_URL + f"/{name}"
    PARAMS = {'auth_key': auth_key, 'url': url}
    r = requests.get(url=URL, params=PARAMS)
    soup = BeautifulSoup(r.content, 'html.parser')
    img_div = soup.find("img", {"class": "_2UpQX"})
    try:
        img_url = img_div["srcset"].split(" ")[-2]
        return img_url
    except TypeError: 
        print(img_div, url)


barbabos_img_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSuNEO1C66cCUvV2jENG8tCKK89rXOGpbY_vA&usqp=CAU"
place_img_list = {place: get_image(place) for place in place_list}
place_img_list["Barbabos"] = barbabos_img_url


with open('/static/csvs/place_img.csv', 'w') as f:
    for key in place_img_list.keys():
        f.write("%s,%s\n"%(key,my_dict[key]))
