FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.4.0


RUN apt update && apt install -y \
  gcc \
  gettext \
  musl-dev \
  && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install -U pip
RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /opt/app

COPY pyproject.toml /opt/app/
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$BUILD_TYPE" = "production" && echo "--without dev") --with sender --no-interaction --no-ansi --no-root

COPY . .