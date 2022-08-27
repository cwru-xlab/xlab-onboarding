# Inbox

## Objectives

- Design a PDA endpoint schema for storing xMail user data
- Understand how to use the Python HAT SDK
- Implement Flask-WTF classes to receive user input when deleting and composing emails
- Implement the Flask inbox endpoint logic
- Implement the inbox page with HTML and Jinja2

## PDA endpoint schema

The tricky part about using PDAs for an email web client is that creating PDA authentication requires an email address.
In other words, if we actually wanted to rely on a user's PDA to store xMail user data, then we would somehow need to
temporarily require a secondary email address of the user in order for them to create a PDA, if they do not have one
already. To make matters more complicated, actually allowing users to send and receive _real_ emails requires an email
server and domain. While we could achieve all of this using a combination of AWS Lambda, Amazon SES, and Amazon Route53,
this kind of functionality is _way_ beyond the scope of this onboarding project.

To keep things simple, and true to the idea that this is only a prototype, we will only use a _single_ PDA to store _
all_ users' data. That is, for a given application namespace (e.g., `xmail`), we can assign each user an endpoint (
i.e., `xmail/<username>`) and store their emails here. We will limit ourselves to this endpoint, rather than creating
sub-endpoints to further organize the user's emails (e.g., spam, deleted, user-created folders, etc.).

The ability to send and delete emails will thus be implemented as follows:

- _Send_: write the `Email` object to the recipient's endpoint
- _Delete_: delete the `Email` object from the authenticated user's endpoint

## Python HAT SDK

Refer to the [README](https://github.com/rtatton/hat-py-sdk/blob/main/README.md) of the hat-py-sdk package for sample
code and explanation.

## Flask-WTF

To receive user input when deleting and composing emails, we will implement
two [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.0.x/) form classes. Refer
to [forms.py](https://github.com/cwru-xlab/xlab-onboarding/blob/ffdf9f8cba5739675f81c339555a3cce101879d1/src/xmail/forms.py#L22-L73)
for their implementation.

## Inbox endpoint

The
Flask [`/inbox` endpoint](https://github.com/cwru-xlab/xlab-onboarding/blob/ffdf9f8cba5739675f81c339555a3cce101879d1/src/xmail/factory.py#L36-L48)
logic is fairly straightforward. Upon receiving a GET request, we will retrieve the user's emails from their PDA
endpoint and render the inbox page. When a POST request is received, we will check to see what _
kind_ of POST request it is (i.e., for deleting emails or for sending an email). If the request is to delete emails, we
will delete the emails that the user has selected in their inbox. Otherwise, we will create an `Email` object and write
it to the recipient's PDA endpoint.

## Inbox frontend

We will keep the inbox page simple: a button to compose an email, a button to delete an email, and a table that contains
all the emails in the user's inbox. We will also keep a simple dropdown menu to allow the user to logout. The modal HTML
that is used to display an inbox email and the email composition form is based
on [this](https://themesberg.com/docs/volt-bootstrap-5-dashboard/components/modals/) code snippet from the AppSeed Volt
Dashboard documentation.