# Getting started

## Objectives

- Install Python and Poetry
- Install Docker
- Clone AppSeed Volt Dashboard repo and copy over assets
- Write Dockerfile and Docker Compose config file

## Remarks

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
tools we will need for development. Please follow the first six sections of
the [first chapter](https://cjolowicz.github.io/posts/hypermodern-python-01-setup)
of the "Hypermodern Python" blog. After reading those sections you should have
Python and Poetry installed. Creating a GitHub repo is not necessary for this
project, but may be of help. If you still want to track any changes, you can
also just [install Git](https://git-scm.com/) without creating a GitHub repo.

Once you have Python and a Poetry virtual environment setup, head over to
the [Docker](https://www.docker.com/get-started/) website to install Docker
Desktop. Please see the [Docker documentation](https://docs.docker.com/) to
learn more about containers.

## Run the application

At this point, you have all you need to run this repo to see the final product.
Simply start Docker, go to the root directory of this project and run

```
docker-compose up --build
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
