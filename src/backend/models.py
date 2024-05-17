import enum

from sqlalchemy.sql import func
from sqlalchemy import create_engine, Column, DateTime, ForeignKey, Integer, Enum, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

# Enums:

class ExerciseCategories(enum.Enum):
    COMPOUND_LIFT = 'Compound Lift'
    ACCESSORY = 'Accessory'
    CARDIO = 'Cardio'

class ConsumableCategories(enum.Enum):
    FOOD = 'Food'
    BEVERAGE = 'Beverage'


# Models:

class Intake(Base):
    __tablename__ = 'intake'

    id = Column(Integer, primary_key=True)
    consumable_id = Column(Integer, ForeignKey("consumable.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    calories = Column(Integer) # computed from Consumable.calories per 100G
    created_at = Column(DateTime, server_default=func.now(), index=True, nullable=False)


class ItemBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class Exercise(ItemBase):
    __tablename__ = 'exercise'

    weight = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)
    category = Column(Enum(ExerciseCategories), nullable=False)


class Consumable(ItemBase):
    __tablename__ = 'consumable'

    calorie_base = Column(Integer, nullable=False)
    category = Column(Enum(ConsumableCategories), nullable=False)



# Triggers:

# from sqlalchemy import event, DDL
# update_task_state = DDL('''\
# CREATE TRIGGER update_task_state UPDATE OF state ON obs
#   BEGIN
#     UPDATE task SET state = 2 WHERE (obs_id = old.id) and (new.state = 2);
#   END;''')
# event.listen(Obs.__table__, 'after_create', update_task_state)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

steak = dict(name='Steak', category=ConsumableCategories.FOOD, calorie_base=100)
coffee = dict(name='Coffee', category=ConsumableCategories.BEVERAGE, calorie_base=1)
intake = dict(consumable_id=1, amount=500, calories=500)
exercise = dict(name='Deadlift', weight=180, reps=1, category=ExerciseCategories.COMPOUND_LIFT)
with SessionLocal() as session:
    steak = Consumable(**steak)
    coffee = Consumable(**coffee)
    record2 = Intake(**intake)
    lift = Exercise(**exercise)
    session.add(steak)
    session.add(coffee)

    session.add(steak)
    session.add(record2)
    session.add(lift)
    session.commit()
    session.flush()
    print(session.query(Consumable).all()[0].name)

