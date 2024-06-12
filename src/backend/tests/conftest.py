import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import domain
from main import app, get_db
from orm import metadata, start_mappers

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create DB:
metadata.drop_all(bind=engine)
metadata.create_all(bind=engine)

# Create tables:
start_mappers()


# Fix pysqlite transaction handling as per:
# https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
@sa.event.listens_for(engine, "connect")
def do_connect(dbapi_connection, connection_record):
    # disable pysqlite's emitting of the BEGIN statement entirely.
    # also stops it from emitting COMMIT before any DDL.
    dbapi_connection.isolation_level = None


@sa.event.listens_for(engine, "begin")
def do_begin(conn):
    # emit our own BEGIN
    conn.exec_driver_sql("BEGIN")


# Nested transactions in SQLite based on:
# https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
@pytest.fixture()
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()

    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @sa.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def beverage_fixture():
    return domain.Consumable(
        name="Test Drink",
        category=domain.CategoryConsumable.BEVERAGE,
        calories=100,
        protein=100,
        carbohydrate=100,
        fat=100,
    )


@pytest.fixture()
def food_fixture():
    return domain.Consumable(
        name="Test Food",
        category=domain.CategoryConsumable.FOOD,
        calories=100,
        protein=100,
        carbohydrate=100,
        fat=100,
    )


@pytest.fixture()
def exercise_fixture():
    return domain.Exercise(
        name="Test Exercise", category=domain.CategoryExercise.COMPOUND_LIFT
    )


@pytest.fixture()
def populated_session(session, food_fixture, exercise_fixture):
    session.add(food_fixture)
    session.add(exercise_fixture)
    session.commit()

    yield session


# Use session fixture, instead of creating a new session
@pytest.fixture()
def test_client(populated_session):
    def override_get_db():
        yield populated_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides = dict()
