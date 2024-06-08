from os import environ
from typing import List

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import add_intake, add_workout, list_consumables, list_exercises
from sqlalchemy import create_engine
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


# Services:


@app.get("/consumable", response_model=List[ConsumableRead])
async def consumables_list(session: Session = Depends(get_db)):
    return list_consumables(session=session)


@app.get("/exercise", response_model=List[ExerciseRead])
async def exercise_list(session: Session = Depends(get_db)):
    return list_exercises(session=session)


@app.post("/intake", response_model=IntakeRead, status_code=201)
async def intake_create(intake: IntakeCreate, session: Session = Depends(get_db)):
    return add_intake(session=session, intake=intake)


@app.post("/workout", response_model=WorkoutRead, status_code=201)
async def workout_create(workout: WorkoutCreate, session: Session = Depends(get_db)):
    return add_workout(session=session, workout=workout)
