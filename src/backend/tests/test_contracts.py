def test_read_item_consumable(test_client) -> None:
    response = test_client.get(url="consumable")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "category": "FOOD",
            "name": "Test Food",
        }
    ]


def test_read_item_exercise(test_client) -> None:
    response = test_client.get(url="exercise")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "category": "Compound Lift",
            "name": "Test Exercise",
        }
    ]


def test_create_workout_entry(test_client) -> None:
    response = test_client.post(
        url="workout",
        json={
            "exercise_id": 1,
            "volume": "120",
            "reps": "5",
            "notes": "test",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "exercise_id": 1,
        "volume": 120,
        "reps": 5,
        "notes": "test",
    }


def test_create_intake_entry(test_client, session) -> None:
    response = test_client.post(
        url="intake",
        json={"consumable_id": "1", "volume": "120"},
    )
    assert response.status_code == 201
    assert response.json() == {"id": 1, "volume": 120}


def test_create_intake_entry_fails_with_invalid_consumable(test_client) -> None:
    response = test_client.post(
        url="intake",
        json={"consumable_id": "1000", "volume": "120", "reps": "5", "notes": "test"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "Integrity Error"}
