import domain


def test_read_item_consumable(test_client) -> None:
    response = test_client.get(url="consumable")
    assert response.status_code == 200
    assert response.json() == []
    # assert response.json() == [
    #     {
    #         "id": 1,
    #         "category": "Beverage",
    #         "name": "Beer",
    #     }
    # ]


def test_read_item_exercise(test_client) -> None:
    response = test_client.get(url="consumable")
    assert response.status_code == 200
    assert response.json() == []
    # assert response.json() == [
    #     {
    #         "id": 1,
    #         "category": "Compound Lift",
    #         "name": "Deadlift",
    #     }
    # ]


def test_create_workout_entry(test_client, session) -> None:
    exercise = domain.Exercise(
        name="Test exercise", category=domain.CategoryExercise.COMPOUND_LIFT
    )
    session.add(exercise)
    session.commit()
    response = test_client.post(
        url="workout",
        json={
            "exercise_id": exercise.id,
            "volume": "120",
            "reps": "5",
            "notes": "test",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "exercise_id": exercise.id,
        "volume": 120,
        "reps": 5,
        "notes": "test",
    }


# def test_create_intake_entry() -> None:
#     response = make_request(
#         url="intake",
#         method="POST",
#         data={"consumable_id": "1", "volume": "120", "reps": "5", "notes": "test"},
#     )
#     assert response.status_code == 201
#     assert response.json() == {"id": 2, "volume": 120}
