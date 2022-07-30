# syntax=docker/dockerfile:1
# Ref: https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
# Ref: https://gist.github.com/soof-golan/6ebb97a792ccd87816c0bda1e6e8b8c2#file-app-py
# If any issues arise using Poetry try using one of the templates provided at:
# https://www.mktr.ai/the-data-scientists-quick-guide-to-dockerfiles-with-examples/
FROM python:3.9-slim AS python
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.1.14
ENV PATH="/root/.local/bin:$PATH"
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim AS app
WORKDIR /app
COPY --from=python /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src/api /app