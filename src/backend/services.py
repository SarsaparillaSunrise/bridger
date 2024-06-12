from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

import validators
from adapters.repository import SQLAlchemyRepository
from domain import Consumable, Exercise, Intake, Workout


def add_intake(
    session: Session, intake: validators.IntakeCreate
) -> validators.IntakeRead:
    repository: SQLAlchemyRepository = SQLAlchemyRepository(session)
    consumable: Consumable = repository.get(
        model=Consumable, record_id=intake.consumable_id
    )
    if not consumable:
        raise HTTPException(status_code=422, detail="Integrity Error")
    record = repository.create(Intake(consumable=consumable, volume=intake.volume))
    record.calculate_intake_presentation_values()
    return validators.IntakeRead(
        consumable=consumable, id=record.id, volume=record.volume
    )


def add_workout(session, workout) -> validators.WorkoutRead:
    repository = SQLAlchemyRepository(session)
    record = repository.create(Workout(**workout.model_dump()))
    return validators.WorkoutRead(
        id=record.id,
        exercise_id=record.exercise_id,
        volume=record.volume,
        reps=record.reps,
        notes=record.notes,
    )


def list_consumables(session) -> validators.ConsumableRead:
    repository = SQLAlchemyRepository(session)
    records = repository.list(Consumable)
    return [validators.ConsumableRead(**c.__dict__) for c in records]


def list_exercises(session):
    repository = SQLAlchemyRepository(session)
    records = repository.list(Exercise)
    return [validators.ExerciseRead(**e.__dict__) for e in records]
