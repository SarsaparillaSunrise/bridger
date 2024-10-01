from datetime import UTC, datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy.orm import registry

from domain import model

metadata = MetaData()
mapper_registry = registry()

consumables = Table(
    "consumables",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("category", Enum(model.CategoryConsumable), nullable=False),
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
    Column("category", Enum(model.CategoryExercise), nullable=False),
)

intakes = Table(
    "intakes",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("consumable_id", ForeignKey("consumables.id"), nullable=False),
    Column("volume", Integer, nullable=False),
    Column("calories", Integer, nullable=False),
)

workouts = Table(
    "workouts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("exercise_id", ForeignKey("exercises.id"), nullable=False),
    Column("volume", Integer, nullable=False),
    Column("reps", Integer, nullable=False),
    Column("notes", String, nullable=True),
    Column("inserted_at", DateTime, nullable=False, default=datetime.now(tz=UTC)),
)


def start_mappers():
    mapper_registry.map_imperatively(class_=model.Consumable, local_table=consumables)
    mapper_registry.map_imperatively(class_=model.Exercise, local_table=exercises)
    mapper_registry.map_imperatively(class_=model.Workout, local_table=workouts)
    mapper_registry.map_imperatively(class_=model.Intake, local_table=intakes)
