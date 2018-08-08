import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
import amalgama

sess = requests.session()


def amalgama_lyrics(artist, song):
    url = amalgama.get_url(artist, song)
    try:
        cached_sess = CacheControl(sess, cache=FileCache('.amalgama'))
        response = cached_sess.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f'{artist}-{song} not found in amalgama {url}')
        return None
    text = amalgama.get_html(response.text)
    return text
