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
RUN apt-get update && apt-get install -y dos2unix
COPY . .

# Ensure Unix-style line endings for scripts
RUN dos2unix ./commands/*.sh

# Add execute bit to commands files
#RUN chmod +x ./commands/*.sh
RUN echo '#!/bin/bash' > /start-wrapper.sh && \
    echo 'cd /app && bash ./commands/start.sh' >> /start-wrapper.sh && \
    chmod +x /start-wrapper.sh

CMD ["/start-wrapper.sh"]

