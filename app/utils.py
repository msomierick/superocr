import collections
import os

from PIL import Image, ExifTags
import pytesseract

from flask import current_app as app


def get_available_image_extensions():
    '''
    Get available image extensions from Pillow's Image object

    :returns: a list of the available image extensions
    '''
    Image.init()
    return [ext.lower()[1:] for ext in Image.EXTENSION]


def is_image_file(filename):
    '''
    Check if filename has valid image extension.

    :param filename: valid name of file as a string

    :returns: True if so otherwise return False
    '''
    allowed = get_available_image_extensions()
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


def is_allowed_file_size(file):
    '''
    Check if file size is within allowed size range.

    :param file: file object in memory

    :returns: True if so otherwise return False
    '''
    limit = app.config['FILE_UPLOAD_LIMIT']
    return os.path.getsize(file) < limit


def bad_request(error):
    '''
    Helper method to handle invalid or bad requests.

    :param error: error string to bake into the response dict.

    :returns: a dict with the error response and a status code.
    '''
    detail = {
        'error': error,
        'status_code': 400
    }
    return detail, 400


def extract_image_text(image_path, lang='eng'):
    '''
    Extract OCR information from image as string

    :param image_path: valid absolute path to image in file system.
    :param lang: OCR language to use. Defaults to eng.

    :returns: the extracted OCR details as a string
    '''
    img = Image.open(image_path)
    return pytesseract.image_to_string(img, lang=lang)


def _convert(data):
    '''
    Byte strings are not JSON serializable. Recursively hunt them and
    decode them.

    :param data: the python object to convert.

    :returns: the passed object with all bytes decoded.
    '''
    if isinstance(data, bytes):
        return data.decode('utf-8')
    elif isinstance(data, collections.Mapping):
        return dict(map(_convert, data.items()))
    elif isinstance(data, (list, tuple)):
        return type(data)(map(_convert, data))
    else:
        return data


def extract_exif_data(image_path):
    '''
    Extract exif metadata from image if any

    :param image_path: valid absolute path to image in file system.

    :returns: image exif metadata extracted from the image as a dict.
    '''
    img = Image.open(image_path)
    info = dict(img.getexif())
    info = _convert(info)
    data = {}
    for k, v in info.items():
        if k in ExifTags.TAGS:
            data[ExifTags.TAGS[k]] = v
    return data
