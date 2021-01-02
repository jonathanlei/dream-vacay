""" get 50 most popular places traveled in the world into a database"""
import requests
from bs4 import BeautifulSoup
import csv


URL = "http://api.proxiesapi.com"
auth_key = "d3c0b94960920290420e953d06cd8839_sr98766_ooPq87"
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
        query_index = img_url.index("?")
        img_url = img_url[:query_index+1]
        return img_url
    except TypeError: 
        print(img_div, url)


barbabos_img_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSuNEO1C66cCUvV2jENG8tCKK89rXOGpbY_vA&usqp=CAU"
place_img_list = [{"place": place, "image_url": get_image(place)} for place in place_list]
# place_img_list["Barbabos"] = barbabos_img_url


keys = place_img_list[0].keys()
with open('static/csvs/places.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(place_img_list)