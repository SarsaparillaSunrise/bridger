from os import environ
from typing import List

from domain import Consumable, Exercise
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Consumable as ConsumableModel
from models import Intake, Workout
from repository import SQLAlchemyRepository
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from validators import (
    ConsumableRead,
    ExerciseRead,
    IntakeCreate,
    IntakeRead,
    WorkoutCreate,
    WorkoutRead,
)

SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autoflush=True, bind=engine)

Base = declarative_base()

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        environ.get("ALLOWED_ORIGIN", ""),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependencies:


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Data:


def insert_record(session, model, data):
    record = model(**data)
    session.add(record)
    try:
        session.flush()
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Record not added")
    session.refresh(record)
    return record


# Services:


@app.get("/consumable", response_model=List[ConsumableRead])
async def consumables_list(session: Session = Depends(get_db)):
    repository = SQLAlchemyRepository(session)
    return repository.list(Consumable)


@app.get("/exercise", response_model=List[ExerciseRead])
async def exercise_list(session: Session = Depends(get_db)):
    repository = SQLAlchemyRepository(session)
    return repository.list(model=Exercise)


@app.post("/intake", response_model=IntakeRead, status_code=201)
async def intake_create(intake: IntakeCreate, session: Session = Depends(get_db)):
    repository = SQLAlchemyRepository(session)
    consumable = repository.get(model=ConsumableModel, record_id=1)
    data = dict(
        calories=consumable.calorie_base / 100 * intake.volume, **intake.model_dump()
    )
    return insert_record(session=session, model=Intake, data=data)


@app.post("/workout", response_model=WorkoutRead, status_code=201)
async def workout_create(workout: WorkoutCreate, session: Session = Depends(get_db)):
    return insert_record(session=session, model=Workout, data=workout.model_dump())
