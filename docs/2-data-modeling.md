# Data modeling

## Objectives

- Learn about Dataswift
- Create a Dataswift developer account
- Learn about third party libraries...
  - Unofficial Dataswift Python SDK
  - pydantic
  - Redis OM Python
  - Flask-Security
- Implement the data classes needed for Flask-Security and xMail

### Remarks

As with the previous module, this module requires a lot of learning new
libraries and concepts. In fact, this is probably the most demanding and
important module for the technical component of the course. Don't worry if
everything does not make sense on first read; it's a lot of new stuff. Just
getting exposed to what all this course involves will help prepare you for the
real work you will be doing for the course.

## Dataswift

### What is Dataswift?

Here are some quotes from Dataswift's OpenCommons page and website that best
describe the purpose and scope of the company:

- "Operator of data server infrastructure technology that decentralises the
  legal ownership of data to individuals and organizations, enabling identity
  authentication / data storage / computation / sharing at a lower cost and risk
  to all parties, with full data portability across geographical territories.
  The infrastructure enables decentralised data networks to be formed between
  individuals and organisations, with secure interactions, verifiable
  information, resulting in improved coordination for the benefit of everyone
  and society" ([source](https://opencommons.org/Dataswift)).
- "Dataswift is a tech-enabled economic solutions company that designs and
  deploys decentralised data mobility networks for its partners and clients to
  own, operate and scale" ([source](https://opencommons.org/Dataswift#Details)).
- "The technology powering Data Accounts is a decentralized data server that
  provides universal ID, personal data protection and grants ownership and
  control of the data to you, the individual. So you control login,
  authentication, verification and licensing of your private, personal data"
  ([source](https://www.dataswift.io/for-individuals)).
- "Dataswift offers technologies that give consumers ownership and control over
  their data to transport the data to other apps and websites; portability of
  personal data built on a rigorous ethical framework and scalable
  technology" ([source](https://www.dataswift.io/for-developers)).

Dataswift inverts the traditional paradigm of data architecture and ownership by
storing user personal data inside Personal Data Accounts (PDAs), rather than
databases owned by the organization/company that owns the application. This
single-sign-on-like experience allows the user to retain legal ownership over
their data across applications. Moreover, it allows developers to simplify their
data architecture by relying on the Dataswift One infrastructure to provide
scalable, privacy-by-default functionality for all aspects that involve managing
user personal data.

### Learning the ecosystem

**For most xLab projects, it is ESSENTIAL that you are familiar with the
concepts and tools included in the Dataswift ecosystem. Just to emphasize how
important this fact is, here it is again: it is ESSENTIAL that you are familiar
with the concepts and tools included in the Dataswift ecosystem.**

To get started, read through
the ["Individuals"](https://www.dataswift.io/for-individuals) and
["Enterprises"](https://www.dataswift.io/for-enterprises). You do not need to
create a PDA for yourself (unless you want to). Next, read the content on
the ["Products"](https://www.dataswift.io/products) page. This will ultimately
lead you to the ["Developers"](https://www.dataswift.io/for-developers) page
where you can find the documentation and API. Do not expect to understand
everything you read all at once. There is a lot of concepts and terminology, so
getting comfortable with the Dataswift ecosystem will likely take some
re-rereading. A helpful reference while you are reading is
their [glossary](https://docs.dataswift.io/knowledge-base/glossary-of-terms).

The developer documentation is extensive. For the purposes of the xLab, you only
need to read through the following sections:

- About Dataswift
- Learn About Dataswift One
- Build on Dataswift One
  - You can skip "Guides" and the other sections under Dataswift One APIs that
    are not "Data API". You will likely need to refer back to the "Guides"
    section once you begin prototype implementation.
- Deploy

For this project, the only thing you really need to know is that a PDA is pretty
much a personal database that an app can use to store app-specific personal
data. If you are familiar with document databases, the Data API may seem
familiar. A PDA is similar in that data is stored as JSON objects and the Data
API provides standard CRUD operations to manage them.

### Developing with PDAs and the Data API

Historically, xLab projects have only required the use of
the [Data API](https://docs.dataswift.io/build/dataswift-one-apis/data-api). If
you are developing in Javascript, it is **highly recommended** that you use the
official [Javascript SDK](https://github.com/dataswift/hat-js-sdk). This will
save you a lot of time and avoid errors. If you are developing in Python, you
can try out an [unofficial SDK](https://github.com/rtatton/hat-py-sdk) that
offers both sync and async support. Because this onboarding project is
Python-based, we will be using this SDK. As of August 2022, this SDK only
supports the authentication and CRUD API endpoints. As the author of this
open-source package, contributions and pull requests are welcomed!

If you have not done so already, you will need to create a developer Dataswift
account for this onboarding project and a project inside your account. This will
give you the credentials and PDA namespace needed to interact with the Dataswift
CRUD API.

## pydantic and Redis OM

pydantic offers "data validation and settings management using python type
annotations. pydantic enforces type hints at runtime, and provides user friendly
errors when data is invalid" ([source](https://pydantic-docs.helpmanual.io/))
. In this project, we will use pydantic directly to define the attributes of
an `Email` object and manage the Flask app configuration.

[Redis OM](https://redis.com/blog/introducing-redis-om-client-libraries/) is an
object-mapping and toolbox library for working with Redis at a high level. The
[Python client](https://github.com/redis/redis-om-python) extends pydantic to
provide
an [active-record](https://martinfowler.com/eaaCatalog/activeRecord.html)
API for manipulating data. For this project, we will use the Python client to
implement a Redis backend for Flask-Security data persistence (i.e., by
extending the `UserMixin`, `RoleMixin`, `Datastore`, and `UserDatastore`
classes). See below for more details.

## Flask-Security

Flask-Security "allows you to quickly add common security mechanisms to your
Flask application" by integrating several other Flask
extensions ([source](https://flask-security-too.readthedocs.io/en/stable/index.html))
. For this project, we will utilize a number of ready-to-use features, including
user login, user registration, password hashing, and session-based
authentication. There are a number of additional features that Flask-Security
offers that are beyond the scope of an MVP (e.g., two-factor authentication).

## xMail implementation

This section of the course will focus on writing and understanding the code
included in
the [`auth.py`](https://github.com/cwru-xlab/xlab-onboarding/blob/main/src/xmail/auth.py)
and [`models.py`](https://github.com/cwru-xlab/xlab-onboarding/blob/main/src/xmail/models.py)
modules.