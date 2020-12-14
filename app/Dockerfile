FROM python:3.8.6-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN mkdir static

COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system

COPY . /app/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh