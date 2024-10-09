import abc
from typing import List

from sqlalchemy import func

from domain.model import Consumable, Exercise, Workout


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


class ExerciseRepository(SQLAlchemyRepository):
    def get_exercises_ordered_by_recent_use(self) -> List[Exercise]:
        latest_workout_subquery = (
            self._session.query(
                Workout.exercise_id, func.max(Workout.inserted_at).label("latest_use")
            )
            .group_by(Workout.exercise_id)
            .subquery()
        )

        query = (
            self._session.query(Exercise, latest_workout_subquery.c.latest_use)
            .outerjoin(
                latest_workout_subquery,
                Exercise.id == latest_workout_subquery.c.exercise_id,
            )
            .order_by(
                latest_workout_subquery.c.latest_use.desc().nullslast(), Exercise.id
            )
        )

        return [exercise for exercise, _ in query.all()]
