import io
import os

from app import create_app


FILE_UPLOAD_LIMIT_IN_MB = 0.001
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_CONFIG = {
    'TESTING': True,
    'UPLOAD_FOLDER': os.path.join(TEST_DIR, 'uploads'),
    'FILE_UPLOAD_LIMIT_IN_MB': FILE_UPLOAD_LIMIT_IN_MB,
    'FILE_UPLOAD_LIMIT': FILE_UPLOAD_LIMIT_IN_MB * 1024 * 1024 
}


def test_config():
    assert not create_app().testing
    assert create_app(TEST_CONFIG).testing


def test_get_request_image_data():
    client = create_app().test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'Upload an image' in response.data


def test_post_request_without_data():
    client = create_app().test_client()
    response = client.post('/')
    assert response.status_code == 400

    expected_json = {'error': 'Post data has no file part', 'status_code': 400}
    assert response.json == expected_json


def test_post_request_invalid_file():
    client = create_app().test_client()

    data = {}
    data['file'] = (io.BytesIO(b'data'), 'invalid.csv')
    response = client.post('/', data=data)

    assert response.status_code == 400

    expected_json = {'error': 'File is not a valid image file', 'status_code': 400}
    assert response.json == expected_json


def test_post_request_large_file():
    client = create_app(TEST_CONFIG).test_client()

    root = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(root, 'images/with_exif.jpg')
    with open(path, 'rb') as f:
        data = {'file': (f, f.name)}
        response = client.post(
            '/',
            data=data,
            content_type='multipart/form-data'
        )

        assert response.status_code == 400

        expected_json = {'error': 'File size too large. Limit is 0.001 MB', 'status_code': 400}
        assert response.json == expected_json


def test_post_request_valid_file():
    client = create_app().test_client()

    root = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(root, 'images/with_exif.jpg')
    with open(path, 'rb') as f:
        data = {'file': (f, f.name)}
        response = client.post(
            '/',
            data=data,
            content_type='multipart/form-data'
        )

        assert response.status_code == 200

        assert response.json['image_text'] == 'No text detected in image'
        assert 'GPSInfo' in response.json['metadata']
        assert 'DateTime' in response.json['metadata']