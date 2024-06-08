from domain import CategoryConsumable, CategoryExercise, Consumable, Exercise, Workout
from sqlalchemy import Column, Enum, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import registry

metadata = MetaData()
mapper_registry = registry()

consumables = Table(
    "consumables",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("category", Enum(CategoryConsumable), nullable=False),
    Column("calories", Integer, nullable=False),
    Column("protein", Integer, nullable=False),
    Column("carbohydrate", Integer, nullable=False),
    Column("fat", Integer, nullable=False),
)


exercises = Table(
    "exercises",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("category", Enum(CategoryExercise), nullable=False),
)


workouts = Table(
    "workouts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("exercise_id", ForeignKey("exercises.id"), nullable=False),
    Column("volume", Integer, nullable=False),
    Column("reps", Integer, nullable=False),
    Column("notes", String, nullable=True),
)


def start_mappers():
    mapper_registry.map_imperatively(class_=Consumable, local_table=consumables)
    mapper_registry.map_imperatively(class_=Exercise, local_table=exercises)
    mapper_registry.map_imperatively(class_=Workout, local_table=workouts)
