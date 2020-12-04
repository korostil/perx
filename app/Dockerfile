FROM python:3.8.6-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN mkdir static

COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system

COPY . /code/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh