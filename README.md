# Installation

## Docker

We will be using docker to avoid environment issues.

`$ docker-compose up`

### To keep in mind

`POSTGRES_PASSWORD` and `POSTGRES_USER`

Extracted from [Postgres Docker image](https://hub.docker.com/_/postgres) documentation:

**POSTGRES_DB**

> This optional environment variable can be used to define a different name for the default database that is created when the image is first started. If it is not specified, then the value of POSTGRES_USER will be used.

## Development

### Create Environment

**macOS/Linux**
```
python3 -m venv .django
```

**Windows:**
```
py -3 -m venv .django
```
## Activate the environment

**macOS/Linux**
```
. .django/bin/activate
```
**Windows:**
```
.django\Scripts\activate
```

## Install 

Install required dependencies:
```
pip install -r requirements.txt
```

