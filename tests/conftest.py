# Credits: https://github.com/ThomasAitken/demo-fastapi-async-sqlalchemy/blob/main/backend/app/conftest.py

import asyncio
from contextlib import ExitStack

import pytest
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from config.index import config as settings
from app.engine.postgresdb import Base, get_db_session, postgresdb as sessionmanager
from main import init_app
from asyncpg import Connection
from fastapi.testclient import TestClient
from pytest_postgresql import factories
from pytest_postgresql.factories.noprocess import postgresql_noproc
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy.testing.entities import ComparableEntity

from config.index import config as env

test_db = factories.postgresql_proc(dbname="test_db", port=5433)


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        # Don't initialize database connection.
        # This is because we want to initialize the database connection manually, so that we can create the test database.
        yield init_app(init_db=False)


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def connection_test(test_db, event_loop):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(user=pg_user, host=pg_host, port=pg_port, dbname=pg_db, version=test_db.version, password=pg_password):
        connection_str = f"postgresql+psycopg://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        sessionmanager.init(connection_str,
                            # {"echo": True, "future": True}
                            )
        yield
        await sessionmanager.close()


@pytest.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, connection_test):
    async def get_db_session_override():
        async with sessionmanager.session() as session:
            yield session

    app.dependency_overrides[get_db_session] = get_db_session_override


@pytest.fixture(scope="function", autouse=True)
async def get_db_session_fixture():
    async with sessionmanager.session() as session:
        yield session
