import services
from validators import (
    ConsumableRead,
    ExerciseRead,
    IntakeCreate,
    WorkoutCreate,
    WorkoutRead,
)


def test_list_consumables(session, food_fixture):
    expected = ConsumableRead(
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
    assert services.list_consumables(session) == [expected]


def test_list_exercises(session, exercise_fixture):
    expected = ExerciseRead(id=1, name="Test Exercise", category="Compound Lift")
    session.add(exercise_fixture)
    session.commit()
    assert services.list_exercises(session) == [expected]


def test_add_workout(session, exercise_fixture):
    session.add(exercise_fixture)
    session.commit()
    workout = WorkoutCreate(exercise_id=1, volume=200, reps=1, notes="Test exercise")
    assert services.add_workout(session=session, workout=workout) == WorkoutRead(
        exercise_id=1, volume=200, reps=1, notes="Test exercise"
    )


def test_add_food_intake(session, food_fixture):
    session.add(food_fixture)
    session.commit()
    intake = IntakeCreate(consumable_id=food_fixture.id, volume=100)
    result = services.add_intake(session=session, intake=intake)
    assert result.id == food_fixture.id
    assert result.volume == 100


def test_add_beverage_intake(session, beverage_fixture):
    session.add(beverage_fixture)
    session.commit()
    intake = IntakeCreate(consumable_id=beverage_fixture.id, volume=330)
    result = services.add_intake(session=session, intake=intake)
    assert result.id == beverage_fixture.id
    assert result.volume == 330
