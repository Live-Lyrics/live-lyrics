import os

from flask import jsonify, request
from flask import current_app as app
from werkzeug.utils import secure_filename

from recognition.helper import allowed_file, recognize
from recognition import recognition


@recognition.route('/blob', methods=['POST'])
def get_blob():
    if 'file' not in request.files:
        return jsonify(status="No file part")
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return recognize(file_path)
    return jsonify({"status": "found"})
