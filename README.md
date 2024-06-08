---
title: Backend
emoji: 🐢
colorFrom: pink
colorTo: blue
sdk: docker
pinned: false
license: mit
app_port: 8000
---

## Getting Started

First, setup the environment with poetry:

> **_Note:_** This step is not needed if you are using the dev-container.

```
poetry shell
poetry install
```

### Start the API server

```
python main.py
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) with your browser to see the Swagger UI of the API.

## Local Postgres database setup

To setup a local postgres database, run:

1. Build the docker image:

```bash
make build-postgres
```

2. Start the docker container:

```bash
make run-postgres
```

## Running Migrations

To generate new migrations, run:

```bash
make generate-migrations migration_title="<name_for_migration>"
```

To locally verify your changes, run:

```bash
make run-migrations
```
