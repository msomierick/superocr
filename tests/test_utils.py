import os

from app import create_app
from app import utils


def test_bad_request():
    actual = utils.bad_request('Invalid input')

    assert actual == ({'error': 'Invalid input', 'status_code': 400}, 400)


def test_valid_image_filename():
    path = 'jondoe.png'

    assert utils.is_image_file(path)


def test_invalid_image_filename():
    path = 'jondoe.csv'

    assert not utils.is_image_file(path)


def test_bytestring_conversion():
    data = {
        'name': b'John Doe',
        'hobbies': [b'Singing', 'Reading', b'Coding'],
        'attrs': {
            'age': 27,
            'country': b'Kenya'
        }
    }

    actual = utils._convert(data)

    # All byte strings should be converted
    expected = data = {
        'name': 'John Doe',
        'hobbies': ['Singing', 'Reading', 'Coding'],
        'attrs': {
            'age': 27,
            'country': 'Kenya'
        }
    }

    assert actual == expected


def test_extract_image_text():
    root = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(root, 'images/with_text.png')

    actual = utils.extract_image_text(path)

    expected = 'ti Jeff Forcier Retweeted\n\nJared Palmer @jaredpalmer - '
    expected += 'Jun 24 \\\nSe, When you merge your own pull request'
    expected += '\n\n \n\nQ 43 TV) 1.1K © 5.5K han'

    assert actual == expected


def test_extract_exif_data():
    root = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(root, 'images/with_exif.jpg')

    actual = utils.extract_exif_data(path)

    assert 'GPSInfo' in actual
    assert 'DateTime' in actual