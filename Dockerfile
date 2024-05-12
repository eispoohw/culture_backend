FROM python:3.11-slim-buster

RUN apt-get update

RUN pip install --upgrade pip

ENV PIP_ROOT_USER_ACTION=ignore

COPY requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir -r /backend/requirements.txt

COPY manage.py /backend

COPY app /backend/app

COPY shop /backend/shop

WORKDIR /backend

EXPOSE 8030