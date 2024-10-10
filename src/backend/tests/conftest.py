import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from adapters.orm import metadata
from config import TEST_DATABASE_URL
from domain import model
from main import app, get_db


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
def beverages():
    return [
        model.Consumable(
            name=f"Test Drink {i}",
            category=model.CategoryConsumable.BEVERAGE,
            calories=100,
            protein=100,
            carbohydrate=100,
            fat=100,
        )
        for i in range(1, 6)
    ]


@pytest.fixture()
def foods():
    return [
        model.Consumable(
            name=f"Test Food {i}",
            category=model.CategoryConsumable.FOOD,
            calories=100,
            protein=100,
            carbohydrate=100,
            fat=100,
        )
        for i in range(1, 6)
    ]


@pytest.fixture(params=["foods", "beverages"])
def consumables(request):
    # This is, as of 2024, the easiest way to parameterise fixtures:
    return request.getfixturevalue(request.param)


@pytest.fixture()
def exercises():
    return [
        model.Exercise(
            name=f"Test Exercise {i}", category=model.CategoryExercise.COMPOUND_LIFT
        )
        for i in range(1, 10)
    ]


@pytest.fixture()
def populated_session(db_session, foods, beverages, exercises):
    db_session.add_all(foods + beverages)
    db_session.add_all(exercises)
    db_session.commit()

    yield db_session


@pytest.fixture()
def test_client(populated_session):
    def override_get_db():
        yield populated_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides = dict()
