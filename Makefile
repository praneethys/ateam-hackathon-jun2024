
include .env

build-postgres:
	docker build -t codepath_project_postgres -f Dockerfile.local.postgres .

run-postgres:
	docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} -e POSTGRES_USER=${POSTGRES_USER} --name ${POSTGRES_DB_NAME} codepath_project_postgres

run-migrations:
	alembic upgrade head

generate-migrations:
	alembic revision --autogenerate -m "$(migration_title)"