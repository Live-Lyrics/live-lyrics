from flask import Flask, render_template, jsonify, request

from vk import sign_in
from lyrics_url import amalgama_url
from lyrics_parser import fetch_amalgama

app = Flask(__name__)
vk = sign_in()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lyrics', methods=['POST'])
def lyric():
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


if __name__ == '__main__':
    app.run(debug=True, port=3333)
