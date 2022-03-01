FROM python:3.8-slim as base

ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED random

RUN pip install --upgrade pip

WORKDIR /app

FROM base as builder

# install and setup poetry
RUN apt update \
    && apt install -y curl \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
ENV PATH=${PATH}:/root/.local/bin

# package & distribution
COPY src/ src/
COPY pyproject.toml poetry.lock ./
COPY README.md .env* ./
RUN python -m venv /venv
RUN . /venv/bin/activate && poetry install --no-interaction --no-dev --no-root
RUN . /venv/bin/activate && poetry build

FROM base

COPY src/ src/
COPY --from=builder /app/dist .
RUN pip install *.whl

# run process as non root
USER 1000:1000

# command to run on container start
ARG env="production"
ENV ENV $env
CMD gunicorn --bind 0.0.0.0:5000 src.app:create_app('${ENV}')
