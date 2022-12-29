import re
import time
import urllib

import lxml
import pandas
import requests
from bs4 import BeautifulSoup

text = pandas.read_csv("player.csv", encoding="ISO-8859-1")
for msg in text["Name"]:
    source = requests.get(
        f"https://www.google.com/search?q=premier+league+{msg}+clear+photo").text
    page = BeautifulSoup(source, "lxml")
    images = page.find_all('img')
    urllib.request.urlretrieve(images[1]['src'], f"image/{msg}.jpg")
    print(f"Downloaded {msg}")
