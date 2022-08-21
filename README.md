# xlab-onboarding

Onboarding project for the xLab Design and Innovation course.

xMail is a simple email client web app prototype with the following features:

- User registration and login with username and password validation
- Sending and receiving emails from other xMail users
- Deleting emails

The intent of this project is to demonstrate how to create a simple software
prototype using libraries, tools, and frameworks that have been used in previous
xLab projects.

## Technical details

xMail is a [Flask](https://flask.palletsprojects.com/en/latest/) web
app. [Flask Security](https://flask-security-too.readthedocs.io/en/stable/index.html)
is used to implement user registration, user login, and credential validation.
The [Python Redis OM](https://redis.io/docs/stack/get-started/tutorials/stack-python/)
library is used to implement a custom
Flask-Security [UserModel, RoleModel](https://flask-security-too.readthedocs.io/en/stable/models.html#models-topic)
,
[Datastore, and UserDatastore](https://flask-security-too.readthedocs.io/en/stable/api.html#datastores)
. User data (i.e., inbox emails) is stored in Dataswift Personal Data Accounts (
PDAs). PDA data is modeled and accessed using
an [unofficial Python SDK](https://github.com/rtatton/hat-py-sdk), which
utilizes [Pydantic](https://pydantic-docs.helpmanual.io/)
. [Pydantic](https://pydantic-docs.helpmanual.io/usage/settings/) is also used
to handle xMail app configuration. The xMail inbox page
utilizes [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.0.x/)
to provide multi-email delete and email composition functionality.

The xMail frontend is derived from
the [AppSeed Flask Bootstrap 5 Volt Dashboard](https://appseed.us/product/volt-dashboard/flask/)
. While much of the client-side functionality is retained, the core handling of
form data is handled by server-side Python code.

[Docker Compose](https://docs.docker.com/compose/) is used to isolate and
orchestrate the Flask app and Redis
database. [Poetry](https://python-poetry.org/) is used to manage Python
dependencies.

## Honorable mentions

Here are some other popular and related tools to this project that could be of
also be of use:

- [Hypermodern Python blog](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/):
  a deep dive on how to develop with Python using modern libraries and
  frameworks
- [ngrok](https://ngrok.com/): allows you to easily host a server from your own
  computer
- [FastAPI](https://fastapi.tiangolo.com/): quickly implement synchronous and
  asynchronous APIs in Python with Pydantic support
- [SQLModel](https://sqlmodel.tiangolo.com/): combines Pydantic
  and [SQLAlchemy](https://www.sqlalchemy.org/) for an even powerful ORM
- [_Git from the Bottom Up_](https://jwiegley.github.io/git-from-the-bottom-up/)

## Additional links

- Using Poetry with
  Docker: [StackOverflow](https://stackoverflow.com/a/72465422)
  and [linked Gist](https://gist.github.com/soof-golan/6ebb97a792ccd87816c0bda1e6e8b8c2#file-app-py)
- [Awesome Docker Compose examples](https://github.com/docker/awesome-compose):
  - [Python/Flask](https://github.com/docker/awesome-compose/tree/master/flask)
  - [Python/Flask/Redis](https://github.com/docker/awesome-compose/tree/master/flask-redis)
  - [Python/FastAPI](https://github.com/docker/awesome-compose/tree/master/fastapi)
- [Redis Stack](https://github.com/redis-stack/redis-stack)
- [Redis Stack with Docker](https://github.com/redis-stack/redis-stack/tree/master/envs/dockers)
- [Redis and FastAPI](https://developer.redis.com/develop/python/fastapi/)
- [Redis and Docker](https://geshan.com.np/blog/2022/01/redis-docker/)