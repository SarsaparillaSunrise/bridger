from domain import validators
from services import handlers


def test_list_consumables(db_session, food_fixture):
    expected = validators.ConsumableRead(
        id=1,
        category="FOOD",
        name="Test Food",
        calories=100,
        protein=100,
        carbohydrate=100,
        fat=100,
    )
    db_session.add(food_fixture)
    db_session.commit()
    assert handlers.list_consumables(db_session) == [expected]


def test_list_exercises(db_session, exercise_fixture):
    expected = validators.ExerciseRead(
        id=1, name="Test Exercise", category="Compound Lift"
    )
    db_session.add(exercise_fixture)
    db_session.commit()
    assert handlers.list_exercises(db_session) == [expected]


def test_add_workout(db_session, exercise_fixture):
    expected = validators.WorkoutRead(
        exercise_id=1, volume=200, reps=1, notes="Test exercise"
    )
    db_session.add(exercise_fixture)
    db_session.commit()

    workout = validators.WorkoutCreate(
        exercise_id=1, volume=200, reps=1, notes="Test exercise"
    )
    assert handlers.add_workout(session=db_session, workout=workout) == expected


def test_add_food_intake(db_session, food_fixture):
    expected = validators.IntakeRead(id=1, volume=100)
    db_session.add(food_fixture)
    db_session.commit()
    intake = validators.IntakeCreate(consumable_id=food_fixture.id, volume=100)
    result = handlers.add_intake(session=db_session, intake=intake)
    assert result == expected


def test_add_beverage_intake(db_session, beverage_fixture):
    expected = validators.IntakeRead(id=1, volume=500)
    db_session.add(beverage_fixture)
    db_session.commit()
    intake = validators.IntakeCreate(consumable_id=beverage_fixture.id, volume=500)
    result = handlers.add_intake(session=db_session, intake=intake)
    assert result == expected
