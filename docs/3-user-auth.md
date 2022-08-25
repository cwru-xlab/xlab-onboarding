# User authentication

## Objectives

- Learn about Flask
- Learn about configuring Flask-Security
- Implement user login
- Implement user registration

## Flask

[Flask](https://flask.palletsprojects.com/en/latest/) is
a [micro-framework](https://flask.palletsprojects.com/en/latest/design/#what-does-micro-mean)
for developing web applications. This document includes links to the relevant parts of Flask's
documentation. If you would prefer a more comprehensive understanding of Flask, work your way
through the full
[documentation](https://flask.palletsprojects.com/en/latest/). At the very least, you should read
through the ["Quickstart"](https://flask.palletsprojects.com/en/latest/quickstart/) section, which
introduces most of what we will need to use Flask. The following are links to other parts of the
documentation that you may want to reference:

- [Application factory pattern](https://flask.palletsprojects.com/en/latest/patterns/appfactories/).
  We'll use this pattern to create an instance of our application.
- [Form Validation with WTForms](https://flask.palletsprojects.com/en/latest/patterns/wtforms/).
  We'll rely
  on [WTForms](https://wtforms.readthedocs.io/en/3.0.x/specific_problems/#rendering-errors) to
  receive user input. We will write a couple of custom forms, but will also indirectly rely on them
  through Flask-Security. We will also
  use [this](https://wtforms.readthedocs.io/en/3.0.x/specific_problems/#rendering-errors) code
  sample to render any errors that occur when validating form data.
- [Set-Cookie options](https://flask.palletsprojects.com/en/latest/security/#set-cookie-options). We
  will override the defaults set by Flask-Security to ensure only HTTPS traffic.
- [Application context](https://flask.palletsprojects.com/en/latest/appcontext/). We will use this
  directly when initializing our application.
- [Configuration handling](https://flask.palletsprojects.com/en/latest/config/). We will configure
  numerous properties for Flask, Flask-Security, and for
  the [Python HAT SDK](https://github.com/rtatton/hat-py-sdk). We will also use pydantic's
  [settings management](https://pydantic-docs.helpmanual.io/usage/settings/) functionality.
- [Error handlers](https://flask.palletsprojects.com/en/latest/errorhandling/#error-handlers). We
  will register several error handlers to utilize the ready-made error pages provided by the AppSeed
  Volt Dashboard template.
- [Jinja2 templates](https://flask.palletsprojects.com/en/latest/templating/). We will augment plain
  HTML with Jinja2 templating functionality to integrate the backend and frontend.
- [Flask design decisions](https://flask.palletsprojects.com/en/latest/design/). This offers some
  additional context about Flask's API design, which might be helpful to know when establishing your
  mental model about how Flask works.

## Configuring Flask-Security

In spite of Flask-Security's extensive functionality, the library is designed to be fairly easy to
learn. For a given Flask application, the behavior of Flask-Security can be customized by overriding
[configuration properties](https://flask-security-too.readthedocs.io/en/stable/configuration.html).
While the sheer number of properties might be overwhelming, this means that adding, removing, and
customizing the security features provided by Flask-Security is pretty much just a matter of
"answering some questions." In particular, Flask-Security
exposes [feature flags](https://flask-security-too.readthedocs.io/en/stable/configuration.html#feature-flags)
that can be toggled to easily enable/disable URL endpoints.

For this project, we will utilize the following features:

- [Session-based authentication](https://flask-security-too.readthedocs.io/en/stable/features.html#session-based-authentication)
- [Password hashing](https://flask-security-too.readthedocs.io/en/stable/features.html#password-hashing)
- [Password validation and complexity](https://flask-security-too.readthedocs.io/en/stable/features.html#password-validation-and-complexity)
- [User registration](https://flask-security-too.readthedocs.io/en/stable/features.html#user-registration)

The following features are not implemented in this prototype, but could feasibly be added:

- [Role/identity-based access](https://flask-security-too.readthedocs.io/en/stable/features.html#role-identity-based-access)
- [Token authentication](https://flask-security-too.readthedocs.io/en/stable/features.html#token-authentication)
- [Two-factor authentication](https://flask-security-too.readthedocs.io/en/stable/features.html#two-factor-authentication)
- [Password reset/recovery](https://flask-security-too.readthedocs.io/en/stable/features.html#password-reset-recovery)
- [Password change](https://flask-security-too.readthedocs.io/en/stable/features.html#password-change)

We will utilize the following security patterns:

- [Authentication and authorization](https://flask-security-too.readthedocs.io/en/stable/patterns.html#authentication-and-authorization)
- [Password validation and complexity](https://flask-security-too.readthedocs.io/en/stable/patterns.html#password-validation-and-complexity)

## Implementation

We utilize
the [Redis backend](https://github.com/cwru-xlab/xlab-onboarding/blob/main/src/xmail/auth.py) that
we implemented in the previous module to persist user credentials.
Checkout [this](https://flask-security-too.readthedocs.io/en/stable/api.html#datastores) page for
information about Flask-Security's `Datastore`
and [this](https://flask-security-too.readthedocs.io/en/stable/models.html#models-topic) page for
information about Flask-Security's data models.

The Python modules we will be writing for this part of the course are

- [`factory.py`](https://github.com/cwru-xlab/xlab-onboarding/blob/main/src/xmail/factory.py):
  Flask application factory function
- [`forms.py`](https://github.com/cwru-xlab/xlab-onboarding/blob/main/src/xmail/forms.py): Custom
  user registration
- [`settings.py`](https://github.com/cwru-xlab/xlab-onboarding/blob/main/src/xmail/settings.py):
  Application configuration

We
will [customize](https://flask-security-too.readthedocs.io/en/stable/customizing.html#customizing)
the registration form so that we can utilize all the default form validation logic without requiring
the input of an email address. Additionally, we will use the AppSeed login and registration HTML
templates in place of the default ones that come with Flask-Security.
