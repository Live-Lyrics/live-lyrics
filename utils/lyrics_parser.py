import requests
from bs4 import BeautifulSoup


def fetch_amalgama(url):
    r = requests.get(url)
    if r.status_code == 404:
        return None
    else:
        bsObj = BeautifulSoup(r.text, "html5lib")
        texts_col = bsObj.find("div", {"class": "texts col"})
        title = texts_col.find("div", {"style": "overflow:hidden;"})
        lyrics = texts_col.find("div", {"id": "click_area"})
        lyrics.find("div", {"id": "quality"}).decompose()
        return "{} \n {}".format(str(title), str(lyrics))


def fetch_lyrsense(url):
    session = requests.Session()
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    r = session.get(url, headers=headers)

    bsObj = BeautifulSoup(r.text, "html5lib")
    table = bsObj.find("table", {"id": "textsTable"})

    [i.decompose() for i in table.findAll("link")]
    [i.decompose() for i in table.findAll("script")]

    table.find("img", {"id": "printPage"})['src'] = '../static/images/lyrsense/print.png'
    table.find("img", {"class": "fontBigger"})['src'] = '../static/images/lyrsense/f-bigger.png'
    table.find("img", {"class": "fontSmaller"})['src'] = '../static/images/lyrsense/f-smaller.png'
    return '{}'.format(table)


if __name__ == '__main__':
    # fetch_lyrsense('https://en.lyrsense.com/foreigner/urgent')
    fetch_lyrsense('https://en.lyrsense.com/adele/hello_adele')
