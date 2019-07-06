import os

from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename

from app.utils import (
    bad_request, extract_exif_data, extract_image_text, is_image_file,
    is_allowed_file_size
)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=['GET', 'POST'])
    def image_data():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                return bad_request('Post data has no file part')

            file = request.files['file']

            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Validate if is a valid image file
            if not is_image_file(save_path):
                return bad_request('File is not a valid image file')

            file.save(save_path)

            # limit file upload size
            if not is_allowed_file_size(save_path):
                limit = app.config['FILE_UPLOAD_LIMIT_IN_MB']
                error = 'File size too large. Limit is {} MB'.format(limit)
                os.remove(save_path)
                return bad_request(error)

            image_text = extract_image_text(save_path)
            image_text = image_text if image_text else 'No text detected in image'

            image_data = {'image_text': image_text}
            image_data['metadata'] = extract_exif_data(save_path)

            return jsonify(image_data)
                                    
        return render_template('index.html')

    return app
