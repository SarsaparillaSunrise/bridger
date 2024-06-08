from domain import Consumable, Exercise
from repository import SQLAlchemyRepository


def list_consumables(session):
    repository = SQLAlchemyRepository(session)
    return repository.list(Consumable)


def list_exercises(session):
    repository = SQLAlchemyRepository(session)
    return repository.list(Exercise)
