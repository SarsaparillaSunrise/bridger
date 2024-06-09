from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from domain import Consumable, Exercise, Intake, Workout
from repository import SQLAlchemyRepository


def add_intake(session: Session, intake: Intake) -> Intake:
    repository: SQLAlchemyRepository = SQLAlchemyRepository(session)
    consumable: Consumable = repository.get(
        model=Consumable, record_id=intake.consumable_id
    )
    if not consumable:
        raise HTTPException(status_code=422, detail="Integrity Error")

    intake = Intake(consumable=consumable, volume=intake.volume)
    return repository.create(intake)


def add_workout(session, workout):
    repository = SQLAlchemyRepository(session)
    return repository.create(Workout(**workout.model_dump()))


def list_consumables(session):
    repository = SQLAlchemyRepository(session)
    return repository.list(Consumable)


def list_exercises(session):
    repository = SQLAlchemyRepository(session)
    return repository.list(Exercise)
