FROM python:3.10-slim

RUN apt-get update && \
    apt-get -y install mc gettext nodejs npm

RUN pip install --upgrade pip
RUN npm install --global less prettier

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN mkdir /home/sites/
WORKDIR /home/sites/
ADD requirements.txt /home/sites/
RUN pip install -r requirements.txt