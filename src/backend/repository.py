import abc


class AbstractRepository(abc.ABC):
    """
    Port for DB adapter
    """

    @abc.abstractmethod
    def __init__(self, session):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, model):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self._session = session

    def list(self, model):
        return self._session.query(model).all()
