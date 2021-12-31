# Installation

## Docker

We will be using docker to avoid environment issues.

Install Docker and Docker-compose from: https://www.docker.com/products/docker-desktop and https://docs.docker.com/compose/install/ respectively.

Then, at the root of the project execute:
```commandline
$ docker-compose up
```

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

# API docs

**POST** {{base_url}}/activities/

JSON payload:
```JSON
{}
```
Sending an empty payload will return activities between 3 days before and 2 weeks after the current time at the request:

Let's assume that to day is 2021-12-31 and in the database we have:
```text
{
        "id": 1,
        "property": ...{}
        ...
        "schedule": "2021-12-27T23:27:31.587888-06:00",
        "status": "active"
    },
    {
        "id": 2,
        "property": ...{}
        ...
        "schedule": "2021-12-30T23:52:06.658795-06:00",
        "status": "active"
    },
    {
        "id": 3,
        "property": ...{}
        ...
        "schedule": "2022-02-01T23:52:06.658795-06:00",
        "status": "active"
    }
```
Then the output will only contain activity with id = 2
Output:
```JSON
[
  {
        "id": 2,
        "property": {
            "id": 1,
            "title": "Prop rest1",
            "address": "adress_rest1",
            "description": "my description rest",
            "status": "enabled",
            "disabled_at": null
        },
        "created_at": "2021-12-30T02:00:33.487657-06:00",
        "updated_at": "2021-12-30T02:00:33.487682-06:00",
        "title": "act",
        "schedule": "2022-01-04T09:30:00-06:00",
        "status": "active"
  }
]
```

Whereas sending a payload with either a data range or the status to filter will return all the records that comply:

Good:
```JSON
{
    "date_init": "2022-01-02",
    "date_end": "2022-01-05",
    "status": "cancelled"
}
```

Good:
```JSON
{
    "status": "cancelled"
}
```

Good:
```JSON
{
    "date_init": "2022-01-02",
    "date_end": "2022-01-05"
}
```

Wrong:
```JSON
{
    "date_init": "2022-01-02",
    "status": "cancelled"
}
```

Wrong:
```JSON
{
    "date_init": "2022-01-02",
    "date_end": "2022-01-05",
    "status": "cancelled",
    "another": "test"
}
```

**PUT** {{base_url}}/activities/:activity_id/

JSON payload:
```JSON
{
    "schedule": "2022-01-04T01:36:00"
}
```
OUTPUT
```JSON
{
    "id": 21,
    "property": {
        "id": 1,
        "title": "Prop rest1",
        "address": "adress_rest1",
        "description": "my description rest",
        "status": "enabled",
        "disabled_at": null
    },
    "created_at": "2021-12-30T02:18:52.547321-06:00",
    "updated_at": "2021-12-30T22:09:28.129625-06:00",
    "title": "act",
    "schedule": "2022-01-04T01:36:00-06:00",
    "status": "active"
}
```

Wrong payload:
```
{
    "schedule": "2022-01-04T01:36:00",
    "test": "test"
}
```


OUTPUT:
```
HTTP Status 400
{
    "code": "not_supported_data_error",
    "message": "not supported data passed at request"
}
```
