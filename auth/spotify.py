import os
import base64
from urllib.parse import urlencode
import json

from flask import Blueprint, request, redirect, jsonify, make_response
import requests

spotify = Blueprint('spotify', __name__)

#  Client Keys
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

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
    "client_id": SPOTIFY_CLIENT_ID
}


@spotify.route("/login")
def login():
    # Auth Step 1: Authorization
    url_args = urlencode(auth_query_parameters)
    print(url_args)
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@spotify.route("/callback")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_code = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_code),
        "redirect_uri": REDIRECT_URI
    }

    base64encoded = base64.b64encode(bytes("{}:{}".format(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET), 'utf-8'))
    headers = {"Authorization": "Basic {}".format(base64encoded.decode('utf-8'))}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    print(access_token)
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    redirect_to_index = redirect("http://localhost:3000/")
    response = make_response(redirect_to_index)
    response.set_cookie('access_token', value=access_token)
    response.set_cookie('refresh_token', value=refresh_token)
    return response


@spotify.route("/refresh_token", methods=['POST'])
def refresh_token():
    # 7. Requesting access token from refresh token
    r = request.get_json()
    refresh_token = r['refresh_token']
    code_payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    base64encoded = base64.b64encode(bytes("{}:{}".format(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET), 'utf-8'))
    headers = {"Authorization": "Basic {}".format(base64encoded.decode('utf-8'))}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)
    response_data = json.loads(post_request.text)
    return jsonify(response_data)
