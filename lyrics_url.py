import requests


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
    url = "http://www.amalgama-lab.com/songs/{}/{}/{}.html".format(first, artist, title)
    return url


if __name__ == '__main__':
    u = amalgama_url('Queen', 'Bicycle Race')
    print(u)
    r = requests.get(u)
    print(r.status_code)
