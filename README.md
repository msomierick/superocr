# Super OCR

This is a Flask project which extracts OCR(Optical Character Recognition) data and Exif
(Exchangeable image file format) data from uploaded images.

Users upload the images and the data is returned as a JSON response.

For the OCR data, the project uses [Google's Tesseract-OCR Engine](https://github.com/tesseract-ocr/tesseract) to recognise and read the text embedded in images, a form of optical character recognition (OCR).

The techstack used comprises the following:

- Python 3(>=3.5)
- Flask
- Google's Tesseract-OCR Engine
- pytesseract, a Python wrapper to Google's Tesseract-OCR Engine.
- Skeleton CSS(http://getskeleton.com/) - for the basic styling
- Docker
- pytest as the unit testing framework
- CircleCI for running the tests
- Gunicorn as the Python WSGI app server

## Workflow

The following is a breakdown of the logic of how the system works when a user uploads a file.

- We perform some validations to ensure whatever is uploaded is what we want. These validations include:
  - Ensure a file is present in the data uploaded.
  - Ensure that file is a valid image file
  - Ensure the file is less than or equal to our allowed limit(5MB)
- If any of these validations fail, the processing terminates and we return an appropriate error
response to the user.
- If the validation is success we save the image in the file system and pass its absolute path
to the OCR Engine and the Exif Data Extractor for processing.
  - The OCR engine recognise and read the text embedded in image(if any) and returns it as dictionary.
  - Exif Data Extractor extracts all exif metadata(if any) and returns it as a dictonary
- The extracted OCR and Exif metadata are combined and returned as a JSON object to the user

## Using the Docker Image

The project exists as a ready to use docker image on Docker hub.

Pull it locally:

`docker pull donmanyo/superocr`

You can run it locally on `PORT 7777` like so, or on any other PORT of your choice:

`docker run -p 7777:5000 donmanyo/superocr`

You can visit the homepage in the browser `http://localhost:7777/` which will display a simple upload form. Use this to test the functionality.

OR better still, you can open the same in Postman and upload the file. Make the image file has the key `file`.

## Local setup

You can also clone the repo from Github and run the project locally without Docker.
The project uses 

Clone the repo:

`git clone https://github.com/msomierick/superocr.git`

Create a virtual environment and install the dependencies(Use Python>=3.5):

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Start the Flask project thus:

`python3 manage.py`

Visit `http://localhost:7777/` either with Postman or a browser to it working.

## Running unit tests

The project uses [pytest](https://docs.pytest.org/en/latest/) as the testing framework and
[Coverage](https://coverage.readthedocs.io/en/v4.5.x/) for generating the test coverage reports.

Run the tests thus, within the cloned repo root folder and the virtual environment activated:

`pytest`

You can view the Coverage HTML test report by open `htmlcov/index.html` in a browser of your choice