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
