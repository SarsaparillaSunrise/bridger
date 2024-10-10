from domain.model import Intake


def test_food_intake_volume_stored_in_milligrams(foods):
    sut = Intake(consumable=foods[0], volume=300)
    assert sut.volume == 300_000


def test_food_intake_volume_presentation_is_in_grams(foods):
    sut = Intake(consumable=foods[0], volume=300)
    assert sut.calculate_intake_presentation_values().volume == 300


def test_beverage_intake_volume_stored_in_millilitres(beverages):
    sut = Intake(consumable=beverages[0], volume=300)
    assert sut.volume == 300


def test_beverage_intake_volume_presentation_is_in_millilitres(beverages):
    sut = Intake(consumable=beverages[0], volume=300)
    assert sut.calculate_intake_presentation_values().volume == 300
