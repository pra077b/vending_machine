FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
RUN mkdir /vending-machine
WORKDIR /vending-machine

RUN apt-get update && apt-get install -y libpq-dev build-essential

COPY . .

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

EXPOSE 8000

