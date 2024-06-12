from dataclasses import dataclass
from enum import Enum


class CategoryConsumable(Enum):
    FOOD = "FOOD"
    BEVERAGE = "BEVERAGE"


class CategoryExercise(Enum):
    COMPOUND_LIFT = "Compound Lift"
    ACCESSORY = "Accessory"
    CARDIO = "Cardio"


@dataclass
class Consumable:
    """
    A consumable item.


    Attributes:
        name: Name
        category: FOOD or DRINK
        calories: the amount of kilocalories in the Consumable
        protein: the amount of protein, expressed in milligrams, in the Consumable
        carbohydrate: the amount of carbohydrate, expressed in milligrams, in the Consumable
        fat: the amount of fat, expressed in milligrams, in the Consumable
    """

    name: str
    category: CategoryConsumable
    calories: int
    protein: int
    carbohydrate: int
    fat: int


@dataclass
class Exercise:
    """
    An exercise


    Attributes:
        name: Name
        category: COMPOUND_LIFT or ACCESSORY
    """

    name: str
    category: CategoryExercise


@dataclass
class Workout:
    """
    Table to store all exercises


    Attributes:
        exercise_id: an Exercise entry
        volume: volume trained
        reps: repetitions performed
        notes: optional notes
    """

    exercise_id: int
    volume: int
    reps: int
    notes: str


class Intake:
    """
    Table to store all consumption

    Intake isn't a value object because some fields are computed.

    Food is given in Grams and is stored in Milligrams
    Beverages are given in Millilitres and stored in Millilitres

    This is currently reconciled for presentation in `calculate_intake_presentation_values`

    Attributes:
        consumable: a Consumable entry
        volume: amount consumed in milligrams if the Consumable category is FOOD; in millitres otherwise
    """

    def __init__(self, consumable: Consumable, volume: int) -> None:
        self._consumable = consumable
        self._volume = volume
        self.consumable_id = consumable.id
        self.volume = self._calculate_total_volume()
        self.calories = self._calculate_total_calories()

    def _calculate_total_calories(self):
        return int(self._consumable.calories * self.volume / 100_000.0)

    def _calculate_total_volume(self):
        if self._consumable.category == CategoryConsumable.FOOD:
            return self._volume * 1000
        return self._volume

    def calculate_intake_presentation_values(self):
        if self._consumable.category == CategoryConsumable.FOOD:
            self.volume /= 1000
        return self
