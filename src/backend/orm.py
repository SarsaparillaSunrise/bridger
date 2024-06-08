from domain import CategoryConsumable, Consumable
from sqlalchemy import Column, Enum, Integer, MetaData, String, Table
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


def start_mappers():
    mapper_registry.map_imperatively(class_=Consumable, local_table=consumables)
