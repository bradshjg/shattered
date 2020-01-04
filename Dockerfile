FROM python:3.6-slim

RUN pip install --no-cache poetry

WORKDIR /src
COPY . /src/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
