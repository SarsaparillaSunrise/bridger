def test_read_consumables(test_client, foods, beverages) -> None:
    def _assert_consumable_contract(response_item, fixture_item):
        assert response_item["id"] is not None
        assert response_item["name"] == fixture_item.name
        assert response_item["category"] == fixture_item.category.value
        assert response_item["calories"] == fixture_item.calories
        assert response_item["protein"] == fixture_item.protein
        assert response_item["carbohydrate"] == fixture_item.carbohydrate
        assert response_item["fat"] == fixture_item.fat

    required_keys = {
        "id",
        "name",
        "category",
        "calories",
        "protein",
        "carbohydrate",
        "fat",
    }
    response = test_client.get(url="/consumable")
    data = response.json()

    response_foods = [item for item in data if item["category"] == "Food"]
    response_beverages = [item for item in data if item["category"] == "Beverage"]

    assert response.status_code == 200
    assert len(data) == len(foods) + len(beverages)
    assert all(item.keys() == required_keys for item in data)
    _assert_consumable_contract(response_foods[0], foods[0])
    _assert_consumable_contract(response_beverages[0], beverages[0])


def test_read_exercises(test_client, exercises) -> None:
    response = test_client.get(url="/exercise")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(exercises)
    assert all(set(item.keys()) == {"id", "name", "category"} for item in data)
    assert data[0]["id"] is not None
    assert data[0]["name"] == exercises[0].name
    assert data[0]["category"] == exercises[0].category.value


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
    assert response.json() == {"id": 1, "consumable_id": 1, "volume": 120}
    assert response.status_code == 201


def test_create_intake_entry_fails_with_invalid_consumable(test_client) -> None:
    response = test_client.post(url="intake", json=dict(consumable_id=1000, volume=100))
    assert response.json() == {"detail": "Integrity Error"}
    assert response.status_code == 422
