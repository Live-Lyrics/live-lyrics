import pprint

from googleapiclient.discovery import build


def main(artist, title):
    service = build("customsearch", "v1",
                    developerKey="AIzaSyA3x---VWKF-n29Z35YXtqnAXTMRXfEWIQ")

    res = service.cse().list(
        q='{} {}'.format(artist, title),
        cx='005361038413828395114:p998mnekm0o',
        num=1
    ).execute()

    url = res['items'][0]['formattedUrl']
    return url


if __name__ == '__main__':
    print(main('adele', 'hello'))
