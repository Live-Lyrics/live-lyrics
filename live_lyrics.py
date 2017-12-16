import os
import json
import base64
from urllib.parse import urlencode

from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests
import discogs_client

from vk import sign_in
from lyrics_url import amalgama_url, lyrsense_url
from lyrics_parser import fetch_amalgama, fetch_lyrsense


app = Flask(__name__, static_folder="static/dist/static", template_folder="static/dist/templates")
# vk = sign_in()

d = discogs_client.Client('ExampleApplication/0.1', user_token=os.environ.get('DISCOGS_TOKEN'))


#################################### - SPOTIFY - #########################
#  Client Keys
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)


# Server-side Parameters
CLIENT_SIDE_URL = "http://localhost"
PORT = 8888
REDIRECT_URI = "{}:{}/callback".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private user-read-currently-playing"
STATE = ""
SHOW_DIALOG_BOOL = True
SHOW_DIALOG_STR = str(SHOW_DIALOG_BOOL).lower()


auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}


@app.route("/login")
def login():
    # Auth Step 1: Authorization
    url_args = urlencode(auth_query_parameters)
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route("/callback")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_code = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_code),
        "redirect_uri": REDIRECT_URI
    }

    base64encoded = base64.b64encode(bytes("{}:{}".format(CLIENT_ID, CLIENT_SECRET), 'utf-8'))
    headers = {"Authorization": "Basic {}".format(base64encoded.decode('utf-8'))}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # redirect_to_index = redirect(url_for('http://127.0.0.1:4200', _external=True))
    redirect_to_index = redirect("/")
    response = app.make_response(redirect_to_index)
    response.set_cookie('access_token', value=access_token)
    response.set_cookie('refresh_token', value=refresh_token)
    return response


@app.route("/refresh_token", methods=['POST'])
def refresh_token():
    # 7. Requesting access token from refresh token
    r = request.get_json()
    refresh_token = r['refresh_token']
    print('refr', refresh_token)
    code_payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    base64encoded = base64.b64encode(bytes("{}:{}".format(CLIENT_ID, CLIENT_SECRET), 'utf-8'))
    headers = {"Authorization": "Basic {}".format(base64encoded.decode('utf-8'))}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)
    response_data = json.loads(post_request.text)
    return jsonify(response_data)

################################### - SPOTIFY - ##########################

def get_youtube_id_from_release(release, title):
    for i in release.videos: 
        if title in i.title:
            youtube_url = i.url
            youtube_id = youtube_url.split('=')[1]
            return youtube_id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/spotify-lyrics', methods=['POST'])
def spotify_lyrics():
    discogs = youtube =  release = None

    r = request.get_json()
    artist = r['artist']
    title = r['title']
    lyrics_provider = r['lyrics_provider']
    additional_information = r['additional_information']
    additional_information = json.JSONDecoder().decode(additional_information)
    if additional_information['discogs']:
        release = d.search('{} - {}'.format(artist, title), type='release')[0]
        discogs = {'year': release.year, 'genres': ', '.join(release.genres),
                   'country': release.country, 'styles': ', '.join(release.styles)}
    
    if additional_information['youtube']:
        if release:
            youtube_id = get_youtube_id_from_release(release, title)
            youtube = {'id': youtube_id}
        else:
            release = d.search('{} - {}'.format(artist, title), type='release')[0]
            youtube_id = get_youtube_id_from_release(release, title)
            youtube = {'id': youtube_id}

    if lyrics_provider == 'amalgama':
        url = amalgama_url(artist, title)
        lyrics = fetch_amalgama(url)
    elif lyrics_provider == 'lyrsense':
        url = lyrsense_url(artist, title)
        lyrics = fetch_lyrsense(url)
    if lyrics:
        return jsonify({"status": "found", "lyrics": lyrics, 'discogs': discogs, 'youtube': youtube})
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
        lyrics = fetch_amalgama(url)
        if lyrics:
            return jsonify({"status": "new", "song": song_name['text'], "lyrics": lyrics})
        else:
            return jsonify({"status": "lyrics not found"})
    else:
        return jsonify({"status": "old"})


if __name__ == "__main__":
    app.run(debug=True, port=8888)
