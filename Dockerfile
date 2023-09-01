# syntax=docker/dockerfile:1.0-experimental
FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /var/local/venv/src
COPY requirements.txt /venv/src/
RUN pip install -r requirements.txt
COPY . venv/src/