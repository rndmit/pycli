FROM docker.io/library/python:3.11-alpine

WORKDIR /opt/pycli

ENV POETRY_VERSION=1.4.2 \
    PATH=/opt/pycli/.venv/bin:${PATH}

RUN apk update --no-cache \
    && apk add \ 
        make \
        curl \
        gcc \
        libressl-dev \
        musl-dev \
        libffi-dev \
    && pip install poetry==${POETRY_VERSION}

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true \
    && poetry install --with dev
