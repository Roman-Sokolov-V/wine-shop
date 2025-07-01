FROM python:3.12-slim
LABEL authors="gnonasis@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN set -x && pip install --no-cache-dir poetry
RUN set -x && poetry config virtualenvs.create false
RUN set -x && poetry install --no-root --without dev
RUN set -x && poetry cache clear . --all --no-interaction && pip cache purge
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN update-ca-certificates

COPY . .
RUN chmod +x ./commands/start.sh