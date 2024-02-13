# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Git
RUN apt-get update && apt-get install -y git

# Option1: Clone the GitHub repository and install from local source, clean up after
RUN git clone --branch 29-package-version-problems https://github.com/RWTH-EBC/AixWeather.git /tmp/aixweather
RUN pip install /tmp/aixweather[full]
RUN rm -rf /tmp/aixweather

# Option2: Install directly via git
# RUN pip install git+https://github.com/RWTH-EBC/AixWeather.git@29-package-version-problems#egg=AixWeather[full]

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt

# Install requirements
RUN pip install -r requirements.txt

RUN mkdir /aixweather

WORKDIR /aixweather

# Mounts the application code to the image
COPY . .

# runs the production server
CMD ["python","manage.py","runserver", "0.0.0.0:8000"]