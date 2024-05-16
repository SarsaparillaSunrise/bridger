import enum
from typing import List

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, DateTime, ForeignKey, Integer, Enum, String, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, sessionmaker, Session


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


# Validators:

class BaseValidator(BaseModel):
    class Config:
        from_attributes = True


class IntakeRead(BaseValidator):
    id: int
    category: str
    name: str


class ExerciseRead(BaseValidator):
    id: int
    category: str
    name: str


# Dependencies:

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Services:


@app.get("/exercise", response_model=List[ExerciseRead])
async def exercise(db: Session = Depends(get_db)):
    return db.query(Exercise).all()


@app.get("/intake", response_model=List[IntakeRead])
async def intake(db: Session = Depends(get_db)):
    return db.query(Consumable).all()
