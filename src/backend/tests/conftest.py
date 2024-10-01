import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from adapters.orm import metadata, start_mappers
from config import TEST_DATABASE_URL
from domain import model
from main import app, get_db

start_mappers()


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(TEST_DATABASE_URL)

    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine, autocommit=False, autoflush=True)
    connection = engine.connect()
    transaction = connection.begin()
    session = Session()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def beverage_fixture():
    return model.Consumable(
        name="Test Drink",
        category=model.CategoryConsumable.BEVERAGE,
        calories=100,
        protein=100,
        carbohydrate=100,
        fat=100,
    )


@pytest.fixture()
def food_fixture():
    return model.Consumable(
        name="Test Food",
        category=model.CategoryConsumable.FOOD,
        calories=100,
        protein=100,
        carbohydrate=100,
        fat=100,
    )


@pytest.fixture()
def exercise_fixture():
    return model.Exercise(
        name="Test Exercise", category=model.CategoryExercise.COMPOUND_LIFT
    )


@pytest.fixture()
def populated_session(db_session, food_fixture, exercise_fixture):
    db_session.add(food_fixture)
    db_session.add(exercise_fixture)
    db_session.commit()

    yield db_session


@pytest.fixture()
def test_client(populated_session):
    def override_get_db():
        yield populated_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides = dict()
