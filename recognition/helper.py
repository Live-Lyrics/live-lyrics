import json
import os

from flask import jsonify

import utils

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def recognize(file_path):
    data = utils.fetch_metadata(file_path)
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
