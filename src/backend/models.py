import enum


from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Enum, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"

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

class ItemBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class TemporalBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now(), index=True, nullable=False)


class Exercise(ItemBase):
    __tablename__ = 'exercise'

    category = Column(Enum(ExerciseCategories), nullable=False)


class Consumable(ItemBase):
    __tablename__ = 'consumable'

    calorie_base = Column(Integer, nullable=False)
    protein_mg = Column(Integer, nullable=False)
    carbs_mg = Column(Integer, nullable=False)
    fat_mg = Column(Integer, nullable=False)
    category = Column(Enum(ConsumableCategories), nullable=False)


class Intake(TemporalBase):
    __tablename__ = 'intake'

    consumable_id = Column(Integer, ForeignKey("consumable.id"), nullable=False)
    volume = Column(Integer, nullable=False)
    calories = Column(Integer, nullable=False)


class Workout(TemporalBase):
    __tablename__ = 'workout'

    exercise_id = Column(Integer, ForeignKey("exercise.id"), nullable=False)
    volume = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)


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

# Consumables:
# steak = dict(name='Steak', category=ConsumableCategories.FOOD, calorie_base=100)
# coffee = dict(name='Coffee', category=ConsumableCategories.BEVERAGE, calorie_base=1)
beer = dict(name='Beer', category=ConsumableCategories.BEVERAGE, calorie_base=100, protein_mg=300, fat_mg=0, carbs_mg=30)

# Intake entry:
# eat_steak = dict(consumable_id=1, volume=500, calories=500)
drink_beer = dict(consumable_id=1, volume=330, calories=130)

# Exercise entry:
exercise = dict(name='Deadlift', category=ExerciseCategories.COMPOUND_LIFT)

# Workout entry:
lift = dict(exercise_id=1, volume=180, reps=1, notes='test note')
noteless_lift = dict(exercise_id=1, volume=180, reps=1)


with SessionLocal() as session:
    # steak = Consumable(**steak)
    # coffee = Consumable(**coffee)
    beer = Consumable(**beer)
    # eat_steak = Intake(**eat_steak)
    eat_steak = Intake(**drink_beer)
    deadlift = Exercise(**exercise)
    lift = Workout(**lift)
    noteless_lift = Workout(**noteless_lift)

    # session.add(steak)
    # session.add(coffee)
    session.add(beer)
    session.add(eat_steak)
    session.add(deadlift)
    session.add(lift)
    session.add(noteless_lift)

    session.commit()
    session.flush()

print('DBs populated')
