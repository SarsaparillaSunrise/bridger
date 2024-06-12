from typing import Optional

from pydantic import BaseModel


class BaseValidator(BaseModel):
    class Config:
        from_attributes = True


class ConsumableRead(BaseValidator):
    id: int
    category: str
    name: str
    calories: int
    protein: int
    carbohydrate: int
    fat: int


class IntakeCreate(BaseValidator):
    consumable_id: int
    volume: int


class IntakeRead(BaseValidator):
    id: int
    volume: int


class ExerciseRead(BaseValidator):
    id: int
    category: str
    name: str


class WorkoutCreate(BaseValidator):
    exercise_id: int
    volume: int
    reps: int
    notes: Optional[str]


class WorkoutRead(BaseValidator):
    exercise_id: int
    volume: int
    reps: int
    notes: Optional[str]
