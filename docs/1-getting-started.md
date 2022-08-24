# Getting started

## Objectives

- Install Python and Poetry
- Install Docker
- Clone the AppSeed Volt Dashboard repo and copy over assets
- Write the Dockerfile and Docker Compose config file

### Remarks

While this project is meant to be an onboarding exercise, it does introduce
several development tools and libraries, i.e., this is more than just another "
Hello world" example. With this in mind, it is recommended that you read through
any linked documentation about the libraries or tools to get the best
understanding about what they do, what value they provide, and how to use them.
There is an abundance of information about all the libraries and tools used in
this project, so no effort is made to restate what is already explained
thoroughly by external sources.

This course does assume you are familiar with Python 3 and general software
development knowledge.

## Install the essentials

As with most software projects, the first thing we need to do is install some
tools that we will need for development. Please follow the first six sections of
the [first chapter](https://cjolowicz.github.io/posts/hypermodern-python-01-setup)
of the "Hypermodern Python" blog. After reading those sections you should have
Python and [Poetry](https://python-poetry.org/docs/) installed. Creating a
GitHub repo is not necessary for this project, but may be of help. If you still
want to track any changes, you can also just [install Git](https://git-scm.com/)
without creating a GitHub repo.

Once you have Python and a Poetry virtual environment
setup, [install Docker](https://www.docker.com/get-started/). Please see
the [Docker documentation](https://docs.docker.com/) to learn more about
containers, the Dockerfile, and Docker Compose.

## Run the application

At this point, you have all you need to run this repo to see the final product.
After cloning this repo, start Docker, go to the repo's root directory, and run

```
docker-compose up
```

This command will look at the `docker-compose.yaml` file and create two
containers, one for the web app and another for the Redis database. Please refer
to the Docker documentation about what each command in that config file means.
When building the `web` service, Docker looks at the Dockerfile and runs those
commands.

Open up a web browser and go to `localhost:8000`. You should see a login page
for the xMail email web client. Try to make an account, login, send emails, and
delete them. It is only possible to send emails to existing xMail users, so you
can either create multiple accounts or just send emails to yourself. This is the
final product we are going to be building.

## Dockerfile and Docker Compose config file

These two files were based on the following sources:

- [StackOverflow: "How to use poetry with docker?"](https://stackoverflow.com/a/72465422)
- Sample Dockerfile and Docker Compose config files from
  the [awesome-compose GitHub repo](https://github.com/docker/awesome-compose):
    - [Flask](https://github.com/docker/awesome-compose/tree/master/flask)
    - [FastAPI](https://github.com/docker/awesome-compose/tree/master/fastapi)
- [README about Docker and Redis Stack](https://github.com/redis-stack/redis-stack/tree/master/envs/dockers)
- ["Using Redis with docker and docker-compose for local development a step-by-step tutorial"](https://geshan.com.np/blog/2022/01/redis-docker/)
    - Note: `command: redis-server --save 20 1` needed to be specified as the
      `REDIS_ARGS` environment variable for the Redis Stack Docker image
      instead.
- [Base Docker image for Flask and Gunicorn](https://github.com/tiangolo/meinheld-gunicorn-flask-docker)
    - And
      ["Using Poetry"](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker#using-poetry)
      from a related Docker image GitHub repo.

For more information about Redis Stack,
see [this page](https://developer.redis.com/create/redis-stack/) from the Redis
documentation.

## AppSeed

This project utilizes
the [AppSeed Flask Bootstrap 5 Volt Dashboard](https://appseed.us/product/volt-dashboard/flask/)
to implement the web frontend.