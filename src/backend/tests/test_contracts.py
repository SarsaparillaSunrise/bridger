def test_read_item_consumable(test_client) -> None:
    expected = dict(
        id=1,
        category="FOOD",
        name="Test Food",
        calories=100,
        protein=100,
        carbohydrate=100,
        fat=100,
    )
    response = test_client.get(url="consumable")
    assert response.json() == [expected]
    assert response.status_code == 200


def test_read_item_exercise(test_client) -> None:
    response = test_client.get(url="exercise")
    [exercise] = response.json()
    assert response.status_code == 200
    assert exercise["category"] == "Compound Lift"
    assert exercise["name"] == "Test Exercise"


def test_create_workout_entry(test_client) -> None:
    response = test_client.post(
        url="workout", json=dict(exercise_id=1, volume=120, reps=5, notes="test")
    )
    workout_entry = response.json()
    assert response.status_code == 201
    assert workout_entry["volume"] == 120
    assert workout_entry["reps"] == 5
    assert workout_entry["notes"] == "test"


def test_create_intake_entry(test_client) -> None:
    response = test_client.post(url="intake", json=dict(consumable_id=1, volume=120))
    assert response.json() == {"id": 1, "volume": 120}
    assert response.status_code == 201


def test_create_intake_entry_fails_with_invalid_consumable(test_client) -> None:
    response = test_client.post(url="intake", json=dict(consumable_id=1000, volume=100))
    assert response.json() == {"detail": "Integrity Error"}
    assert response.status_code == 422
