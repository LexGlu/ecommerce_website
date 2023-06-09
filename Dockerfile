FROM python:3.11.3-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/app

# Pip is upgraded and the libpq-dev and gcc packages are installed using apt-get.
# The libpq-dev package is needed to install the psycopg2 package, which is a PostgreSQL adapter for Python.
RUN pip install --upgrade pip && apt-get update &&  apt-get -y install libpq-dev gcc
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./
