FROM ubuntu:18.04

# set python 3.6
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:jonathonf/python-3.6

# initial update
RUN apt-get update -y

# install python3.6 and related libs
RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv && \
    apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade && \
    python3.6 -m pip install wheel

# install the beauty - tesseract-ocr
RUN apt-get update && apt-get install -y tesseract-ocr

# set environment variables
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV FLASK_APP app

# create the working dir
RUN mkdir /app

# Set the working directory to /app
WORKDIR /app

# Copy
COPY ./requirements.txt /app/requirements.txt 

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the Flask application with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "manage:app"]
