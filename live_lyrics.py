import os
import json

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import discogs_client

from utils import lyrics_url
from utils import lyrics_parser
from utils import discogs
from utils import acr_identify
from auth.vk import vk_sign_in

from auth.spotify import spotify

UPLOAD_FOLDER = 'static/mp3'
ALLOWED_EXTENSIONS = set(['mp3', 'wav', 'ogg'])

app = Flask(__name__)
app.register_blueprint(spotify)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# vk = vk_sign_in()

d = discogs_client.Client('ExampleApplication/0.1', user_token=os.environ.get('DISCOGS_TOKEN'))

acr_cloud_config = {
    'host': os.environ.get('HOST'),
    'access_key': os.environ.get('ACCESS_KEY'),
    'access_secret': os.environ.get('ACCESS_SECRET'),
    'timeout': 5  # seconds
}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def recognize(file_path):
    data = acr_identify.fetch_metadata(file_path)
    if data['status']['code'] == 0:
        filename_w_ext = os.path.basename(file_path)
        json_filename, file_extension = os.path.splitext(filename_w_ext)
        with open(f'static/json/{json_filename}.json', 'w', encoding='utf8') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)

        artist = data['metadata']['music'][0]['artists'][0]['name']
        title = data['metadata']['music'][0]['title']
        return jsonify({"artist": artist, 'title': title})
    else:
        return 'songs not found'


@app.route('/blob', methods=['POST'])
def getblob():
    if 'file' not in request.files:
        return jsonify(status="No file part")
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return recognize(file_path)
    return jsonify({"status": "found"})


@app.route('/spotify-lyrics', methods=['POST'])
def spotify_lyrics():
    discogs_data = youtube = release = None

    r = request.get_json()
    artist = r['artist']
    title = r['title']
    lyrics_provider = r['lyrics_provider']
    additional_information = r['additional_information']
    additional_information = json.JSONDecoder().decode(additional_information)
    if additional_information['discogs']:
        release = d.search('{} - {}'.format(artist, title), type='release')[0]
        discogs_data = {'year': release.year, 'genres': ', '.join(release.genres),
                        'country': release.country, 'styles': ', '.join(release.styles)}
    
    if additional_information['youtube']:
        if release:
            youtube_id = discogs.get_youtube_id_from_release(release, title)
            youtube = {'id': youtube_id}
        else:
            release = d.search('{} - {}'.format(artist, title), type='release')[0]
            youtube_id = discogs.get_youtube_id_from_release(release, title)
            youtube = {'id': youtube_id}

    if lyrics_provider == 'amalgama':
        url = lyrics_url.amalgama_url(artist, title)
        lyrics = lyrics_parser.fetch_amalgama(url)
    elif lyrics_provider == 'lyrsense':
        url = lyrics_url.lyrsense_url(artist, title)
        lyrics = lyrics_parser.fetch_lyrsense(url)
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
