import os

import requests
from googleapiclient.discovery import build


def vk_normalize(s):
    parentheses = s[s.find('('):s.find(')') + 1]
    s = s.replace(parentheses, '')

    sq_brackets = s[s.find('['):s.find(']') + 1]
    s = s.replace(sq_brackets, '')

    s = s.lstrip()
    s = s.rstrip()
    return s


def build_url(s):
    s = s.lower()
    s = s.replace(' ', '_')
    s = s.replace("'", '_')
    s = s.replace("__", '_')
    return s


def amalgama_url(artist, title):
    artist, title = map(vk_normalize, [artist, title])
    artist, title = map(build_url, [artist, title])
    first = artist[0]
    url = "http://www.amalgama-lab.com/songs/{}/{}/{}.html".format(
        first, artist, title)
    return url


# def build_lyrsense_url(s):
#     s = s.lower()
#     s = s.replace(' ', '_')
#     s = s.replace("'", '')
#     s = s.replace("__", '_')
#     return s


# def lyrsense_url(artist, title):
#     artist, title = map(vk_normalize, [artist, title])
#     artist, title = map(build_lyrsense_url, [artist, title])
#     url = "https://en.lyrsense.com/{}/{}".format(artist, title)
#     return url


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


if __name__ == '__main__':
    # u = amalgama_url('Queen', 'Bicycle Race')
    # u = lyrsense_url('Queen', 'Bicycle Race')
    # url = amalgama_url('Kylie Minogue', 'Love At First Sight')
    # u = lyrsense_url('Kylie Minogue', 'Love At First Sight')
    # url = amalgama_url('Kylie Minogue', 'Confide in Me')
    # u = lyrsense_url('Kylie Minogue', 'Confide in Me')
    # url = amalgama_url('Kylie Minogue', 'Come Into My World (Radio Edit)')
    # u = lyrsense_url('Kylie Minogue', 'Come Into My World (Radio Edit)')
    # url = amalgama_url('Kylie Minogue', "Can't Get You Out Of My Head (2001)")
    # u = lyrsense_url('Kylie Minogue', "Can't Get You Out Of My Head (2001)")
    # url = amalgama_url('Iggy Pop', "The Passenger")
    # u = lyrsense_url('Iggy Pop', "The Passenger")
    # url = amalgama_url("Rag'n'Bone Man", "Human (Rudimental Remix)")
    # url = amalgama_url("Rammstein", "Sonne [Original]")
    # url = amalgama_url("Bryan Adams", "Summer of '69")
    # url = amalgama_url("Rag'n'Bone Man", "Human  (original)")
    u = lyrsense_url("Rag'n'Bone Man", "Human (Rudimental Remix)")
    print(u)
    r = requests.get(u)
    print(r.status_code)
