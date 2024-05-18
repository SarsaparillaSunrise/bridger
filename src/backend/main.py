import enum
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, DateTime, ForeignKey, Integer, Enum, String, Text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from models import Consumable, Exercise, Intake, Workout


SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autoflush=True, bind=engine)

Base = declarative_base()

app = FastAPI(debug=True)

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

# Validators:

class BaseValidator(BaseModel):
    class Config:
        from_attributes = True


class IntakeRead(BaseValidator):
    id: int
    volume: int
    created_at: datetime


class ExerciseRead(BaseValidator):
    id: int
    category: str
    name: str


class WorkoutCreate(BaseValidator):
    exercise_id: int
    weight: int
    reps: int
    notes: Optional[str]


class IntakeCreate(BaseValidator):
    consumable_id: int
    volume: int


class WorkoutRead(BaseValidator):
    exercise_id: int
    weight: int
    reps: int
    notes: Optional[str]

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


def insert_record(session, model, data):
    record = model(**data)
    session.add(record)
    try:
        session.flush()
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail='Record not added')
    session.refresh(record)
    return record


@app.post("/intake", response_model=IntakeRead, status_code=201)
async def intake_create(intake: IntakeCreate, session: Session = Depends(get_db)):
    return insert_record(session=session, model=Intake, data=intake.model_dump())


@app.post("/workout", response_model=WorkoutRead, status_code=201)
async def workout_create(workout: WorkoutCreate, session: Session = Depends(get_db)):
    return insert_record(session=session, model=Workout, data=workout.model_dump())
