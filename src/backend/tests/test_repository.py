from domain import Consumable
from repository import SQLAlchemyRepository


def test_list_consumables(session):
    repository = SQLAlchemyRepository(session)
    assert repository.list(Consumable) == []
