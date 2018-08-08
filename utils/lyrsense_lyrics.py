import os

import requests
# from bs4 import BeautifulSoup
# from googleapiclient.discovery import build


def lyrsense_url(artist, title):
    developerKey = os.environ.get('GOOGLE_SEARCH_API')
    service = build("customsearch", "v1", developerKey=developerKey)

    res = service.cse().list(
        q='{} {}'.format(artist, title),
        cx='005361038413828395114:p998mnekm0o',
        num=1
    ).execute()

    url = res['items'][0]['formattedUrl']
    return url


def fetch_lyrsense(url):
    session = requests.Session()
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
    r = session.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html5lib")
    table = soup.find("table", {"id": "textsTable"})

    [i.decompose() for i in table.findAll("link")]
    [i.decompose() for i in table.findAll("script")]

    table.find("img", {"id": "printPage"})['src'] = '../static/images/lyrsense/print.png'
    table.find("img", {"class": "fontBigger"})['src'] = '../static/images/lyrsense/f-bigger.png'
    table.find("img", {"class": "fontSmaller"})['src'] = '../static/images/lyrsense/f-smaller.png'
    return '{}'.format(table)
