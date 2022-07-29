# syntax=docker/dockerfile:1
# Ref: https://github.com/tiangolo/meinheld-gunicorn-flask-docker
# Ref: https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker#using-poetry
# Ref: https://gist.github.com/soof-golan/6ebb97a792ccd87816c0bda1e6e8b8c2#file-app-py
FROM python:3.9-slim as python
WORKDIR /tmp
RUN apt-get update && apt-get install -y --no-install-recommends curl
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.1.14
ENV PATH="/root/.local/bin:$PATH"
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM tiangolo/meinheld-gunicorn-flask:python3.9 AS app
WORKDIR /app
COPY --from=python /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src/web /app
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000" ,"main:app"]