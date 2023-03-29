FROM python:3.10-slim

ARG BUILD_TYPE

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV POETRY_VERSION=1.4.0

RUN apt update && apt install -y \
  gcc \
  gettext \
  musl-dev \
  && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install -U pip
RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /code
COPY pyproject.toml /code/
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$BUILD_TYPE" = "production" && echo "--without dev") --no-interaction --no-ansi --no-root

COPY . .
ENTRYPOINT ["pytest", "-s", "./tests/functional/src"]
