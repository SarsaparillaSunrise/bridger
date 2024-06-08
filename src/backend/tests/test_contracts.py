from utils import make_request


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


def test_create_workout_entry() -> None:
    response = make_request(
        url="workout",
        method="POST",
        data={"exercise_id": "1", "volume": "120", "reps": "5", "notes": "test"},
    )
    assert response.status_code == 201
    assert response.json() == {
        "exercise_id": 1,
        "volume": 120,
        "reps": 5,
        "notes": "test",
    }


def test_create_intake_entry() -> None:
    response = make_request(
        url="intake",
        method="POST",
        data={"consumable_id": "1", "volume": "120", "reps": "5", "notes": "test"},
    )
    assert response.status_code == 201
    assert response.json() == {"id": 2, "volume": 120}
