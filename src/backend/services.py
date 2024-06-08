from domain import Consumable, Exercise, Workout
from repository import SQLAlchemyRepository


def add_workout(session, workout):
    repository = SQLAlchemyRepository(session)
    return repository.add(Workout(**workout.model_dump()))


def list_consumables(session):
    repository = SQLAlchemyRepository(session)
    return repository.list(Consumable)


def list_exercises(session):
    repository = SQLAlchemyRepository(session)
    return repository.list(Exercise)
