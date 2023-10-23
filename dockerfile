# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /aixweather

WORKDIR /aixweather

# Mounts the application code to the image
COPY . .

# runs the production server
CMD ["python","manage.py","runserver", "0.0.0.0:8000"]