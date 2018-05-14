
def get_youtube_id_from_release(release, title):
    for i in release.videos:
        if title in i.title:
            youtube_url = i.url
            youtube_id = youtube_url.split('=')[1]
            return youtube_id
