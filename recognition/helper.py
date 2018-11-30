import json
import os

from flask import jsonify
from acrcloud import ACRCloud

ACR_access_key = os.environ.get('ACR_ACCESS_KEY')
ACR_access_secret = bytes(os.environ.get('ACR_ACCESS_SECRET'), 'utf-8')
acr = ACRCloud('eu-west-1.api.acrcloud.com', ACR_access_key, ACR_access_secret)

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def recognize(file_path):
    data = acr.identify(file_path)
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
