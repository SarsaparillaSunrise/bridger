import abc

from domain.model import Consumable


class AbstractRepository(abc.ABC):
    """
    Port for SQLAlchemy Adapter
    """

    @abc.abstractmethod
    def __init__(self, session):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, model):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, model, record_id):
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, record):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self._session = session

    def list(self, model):
        return self._session.query(model).all()

    def get(self, model: Consumable, record_id: int) -> Consumable:
        return self._session.get(model, record_id)

    def create(self, record):
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        return record
