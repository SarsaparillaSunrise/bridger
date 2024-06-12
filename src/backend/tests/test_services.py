from domain import validators
from services import handlers


def test_list_consumables(session, food_fixture):
    expected = validators.ConsumableRead(
        id=1,
        category="FOOD",
        name="Test Food",
        calories=100,
        protein=100,
        carbohydrate=100,
        fat=100,
    )
    session.add(food_fixture)
    session.commit()
    assert handlers.list_consumables(session) == [expected]


def test_list_exercises(session, exercise_fixture):
    expected = validators.ExerciseRead(
        id=1, name="Test Exercise", category="Compound Lift"
    )
    session.add(exercise_fixture)
    session.commit()
    assert handlers.list_exercises(session) == [expected]


def test_add_workout(session, exercise_fixture):
    expected = validators.WorkoutRead(
        exercise_id=1, volume=200, reps=1, notes="Test exercise"
    )
    session.add(exercise_fixture)
    session.commit()

    workout = validators.WorkoutCreate(
        exercise_id=1, volume=200, reps=1, notes="Test exercise"
    )
    assert handlers.add_workout(session=session, workout=workout) == expected


def test_add_food_intake(session, food_fixture):
    expected = validators.IntakeRead(id=1, volume=100)
    session.add(food_fixture)
    session.commit()
    intake = validators.IntakeCreate(consumable_id=food_fixture.id, volume=100)
    result = handlers.add_intake(session=session, intake=intake)
    assert result == expected


def test_add_beverage_intake(session, beverage_fixture):
    expected = validators.IntakeRead(id=1, volume=500)
    session.add(beverage_fixture)
    session.commit()
    intake = validators.IntakeCreate(consumable_id=beverage_fixture.id, volume=500)
    result = handlers.add_intake(session=session, intake=intake)
    assert result == expected
