from domain import Intake


def test_beverage_intake_volume_stored_in_millilitres(beverage_fixture):
    intake = Intake(consumable=beverage_fixture, volume=300)
    assert intake.volume == 300


def test_food_intake_volume_stored_in_milligrams(food_fixture):
    intake = Intake(consumable=food_fixture, volume=300)
    assert intake.volume == 300_000


def test_food_intake_volume_presentation_is_in_grams(food_fixture):
    intake = Intake(consumable=food_fixture, volume=300)
    assert intake.calculate_intake_presentation_values().volume == 300


def test_beverage_intake_volume_presentation_is_in_millilitres(beverage_fixture):
    intake = Intake(consumable=beverage_fixture, volume=300)
    assert intake.calculate_intake_presentation_values().volume == 300
