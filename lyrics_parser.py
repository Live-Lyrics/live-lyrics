import requests
from bs4 import BeautifulSoup


def fetch_amalgama(url):
    r = requests.get(url)
    if r.status_code == 404:
        return None
    else:
        bsObj = BeautifulSoup(r.text, "html.parser")
        texts_col = bsObj.find("div", {"class": "texts col"})
        title = texts_col.find("div", {"style": "overflow:hidden;"})
        lyrics = texts_col.find("div", {"id": "click_area"})
        lyrics.find("div", {"id": "quality"}).decompose()
        return "{} \n {}".format(str(title), str(lyrics))
