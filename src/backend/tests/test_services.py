import time

from domain import model, validators
from services import handlers


def test_list_consumables(db_session, foods):
    db_session.add_all(foods)
    db_session.commit()

    result = handlers.list_consumables(db_session)

    assert len(result) == len(foods)
    for actual, expected in zip(result, foods):
        assert actual.id is not None
        assert actual.name == expected.name
        assert actual.category == expected.category.value
        assert actual.calories == expected.calories
        assert actual.protein == expected.protein
        assert actual.carbohydrate == expected.carbohydrate
        assert actual.fat == expected.fat


def test_list_exercises_ordered_by_recent_use(db_session, exercises):
    db_session.add_all(exercises)
    db_session.commit()
    expected_order = [3, 2, 1, 4]
    workout_data = [(1, 100), (2, 200), (3, 300)]

    for exercise_id, volume in workout_data:
        db_session.add(
            model.Workout(exercise_id=exercise_id, volume=volume, reps=10, notes="")
        )
        db_session.commit()
        time.sleep(0.1)  # 100ms delay

    result = handlers.list_exercises_ordered_by_recent_use(db_session)

    assert [e.id for e in result][:4] == expected_order


def test_add_workout_returns_correct_data(db_session, exercises):
    db_session.add_all(exercises)
    db_session.commit()
    exercise = db_session.query(model.Exercise).first()

    workout = validators.WorkoutCreate(
        exercise_id=exercise.id, volume=200, reps=1, notes="Test exercise"
    )

    result = handlers.add_workout(session=db_session, workout=workout)

    assert result.id is not None
    assert result.exercise_id == exercise.id
    assert result.volume == 200
    assert result.reps == 1
    assert result.notes == "Test exercise"


def test_add_intake_returns_correct_data(db_session, consumables):
    db_session.add_all(consumables)
    db_session.commit()
    consumable = db_session.query(model.Consumable).first()
    intake = validators.IntakeCreate(consumable_id=consumable.id, volume=100)

    result = handlers.add_intake(session=db_session, intake=intake)

    assert result.id is not None
    assert result.volume == 100
    assert result.consumable_id == consumable.id


def test_add_workout_persists_correct_data(db_session, exercises):
    db_session.add_all(exercises)
    db_session.commit()
    exercise = db_session.query(model.Exercise).first()

    workout = validators.WorkoutCreate(
        exercise_id=exercise.id, volume=200, reps=1, notes="Test exercise"
    )

    result = handlers.add_workout(session=db_session, workout=workout)

    db_workout = db_session.query(model.Workout).filter_by(id=result.id).first()
    assert db_workout is not None
    assert db_workout.exercise_id == exercise.id
    assert db_workout.volume == 200
    assert db_workout.reps == 1
    assert db_workout.notes == "Test exercise"
    assert db_workout.exercise_id == exercise.id


def test_add_intake_persists_correct_data(db_session, consumables):
    db_session.add_all(consumables)
    db_session.commit()
    consumable = db_session.query(model.Consumable).first()
    intake = validators.IntakeCreate(consumable_id=consumable.id, volume=100)

    result = handlers.add_intake(session=db_session, intake=intake)

    db_intake = db_session.query(model.Intake).filter_by(id=result.id).first()
    assert db_intake is not None
    assert db_intake.consumable_id == consumable.id
    assert db_intake.volume == 100
