import os
import json

from flask import Flask, jsonify, request
import discogs_client

import utils
# from auth.vk import vk_sign_in
from auth.spotify import spotify
from recognition import recognition

UPLOAD_FOLDER = 'static/mp3'

app = Flask(__name__)
app.register_blueprint(spotify)
app.register_blueprint(recognition)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# vk = vk_sign_in()

discogs = discogs_client.Client('ExampleApplication/0.1', user_token=os.environ.get('DISCOGS_TOKEN'))


@app.route('/spotify-lyrics', methods=['POST'])
def spotify_lyrics():
    discogs_data = youtube = release = lyrics = None

    r = request.get_json()
    artist = r['artist']
    title = r['title']
    lyrics_provider = r['lyrics_provider']
    additional_information = r['additional_information']
    additional_information = json.JSONDecoder().decode(additional_information)
    if additional_information['discogs']:
        release = discogs.search('{} - {}'.format(artist, title), type='release')[0]
        discogs_data = {'year': release.year, 'genres': ', '.join(release.genres),
                        'country': release.country, 'styles': ', '.join(release.styles)}
    
    if additional_information['youtube']:
        if release:
            youtube_id = utils.get_youtube_id_from_release(release, title)
            youtube = {'id': youtube_id}
        else:
            release = discogs.search('{} - {}'.format(artist, title), type='release')[0]
            youtube_id = utils.get_youtube_id_from_release(release, title)
            youtube = {'id': youtube_id}

    artist, title = map(utils.normalize, [artist, title])

    if lyrics_provider == 'amalgama':
        lyrics = utils.amalgama_lyrics(artist, title)
    elif lyrics_provider == 'lyrsense':
        url = utils.lyrsense_url(artist, title)
        lyrics = utils.fetch_lyrsense(url)
    if lyrics:
        return jsonify({"status": "found", "lyrics": lyrics, 'discogs': discogs_data, 'youtube': youtube})
    else:
        return jsonify({"status": "lyrics not found"})


@app.route('/vk-lyrics', methods=['POST'])
def vk_lyrics():
    user_id = request.cookies.get('id')
    old_song_name = request.form['old_song_name']
    song_name = vk.status.get(user_id=user_id)
    if 'audio' not in song_name:
        return jsonify({"status": "empty"})
    elif ('audio' in song_name) and (old_song_name != song_name['text']):
        artist = song_name['audio']['artist']
        title = song_name['audio']['title']
        url = amalgama_url(artist, title)
        lyrics = lyrics_parser.fetch_amalgama(url)
        if lyrics:
            return jsonify({"status": "new", "song": song_name['text'], "lyrics": lyrics})
        else:
            return jsonify({"status": "lyrics not found"})
    else:
        return jsonify({"status": "old"})


if __name__ == "__main__":
    app.run(debug=True, port=8888)
