import collections
import os

from PIL import Image, ExifTags
import pytesseract

from flask import current_app as app


def get_available_image_extensions():
    '''
    Get available image extensions from Pillow's Image object
    '''
    Image.init()
    return [ext.lower()[1:] for ext in Image.EXTENSION]


def is_image_file(filename):
    '''
    Check if filename has valid image extension.

    Return True if so otherwise return False
    '''
    allowed = get_available_image_extensions()
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


def is_allowed_file_size(file):
    '''
    Check if file size is within allowed size range.

    Return True if so otherwise return False
    '''
    limit = app.config['FILE_UPLOAD_LIMIT']
    return os.path.getsize(file) < limit


def bad_request(error):
    '''
    Helper method returning response when we get an invalid or bad request
    '''
    detail = {
        'error': error,
        'status_code': 400
    }
    return detail, 400


def extract_image_text(image_path, lang='eng'):
    '''
    Extract OCR information from image as string
    '''
    return pytesseract.image_to_string(image_path, lang=lang)


def _convert(data):
    '''
    Byte strings are not JSON serializable.

    Recursively hunt them and decode them to unicode strings.
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
    '''
    img = Image.open(image_path)
    info = dict(img.getexif())
    info = _convert(info)
    data = {}
    for k, v in info.items():
        if k in ExifTags.TAGS:
            data[ExifTags.TAGS[k]] = v
    return data
