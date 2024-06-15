FROM python:3.11.0-slim

WORKDIR /app

ENV PIP_DEFAULT_TIMEOUT=400 \
    # Allow statements and log messages to immediately appear
    PYTHONUNBUFFERED=1 \
    # disable a pip version check to reduce run-time & log-spam
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # cache is useless in docker image, so disable to reduce image size
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.6.0 \
    AWS_DEFAULT_REGION=ap-south-1 \
    PATH="/root/.local/bin:$PATH" \
    POETRY_VERSION=1.6.0

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    libpq-dev \
    gcc \
    curl 

COPY poetry.lock pyproject.toml /app/

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_VERSION} python3 - \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev

COPY . /app

EXPOSE 6379