FROM python:3.12-slim
LABEL authors="gnonasis@gmail.com"

ENV PYTHONUNBUFFERED=1
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    build-essential \
#    git \
#    libpq-dev \
#    libjpeg-dev \
#    zlib1g-dev \
#    # Додайте інші залежності, якщо ваш проект їх потребує.
#    # Наприклад, libssl-dev для деяких мережевих пакетів, якщо вони використовуються.
#    && rm -rf /var/lib/apt/lists/*

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

COPY . .
#
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]