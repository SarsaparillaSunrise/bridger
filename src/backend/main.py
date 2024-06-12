from os import environ
from typing import List

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from domain import validators
from services import handlers

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


@app.get("/consumable", response_model=List[validators.ConsumableRead])
async def consumables_list(session: Session = Depends(get_db)):
    return handlers.list_consumables(session=session)


@app.get("/exercise", response_model=List[validators.ExerciseRead])
async def exercise_list(session: Session = Depends(get_db)):
    return handlers.list_exercises(session=session)


@app.post("/intake", response_model=validators.IntakeRead, status_code=201)
async def intake_create(
    intake: validators.IntakeCreate, session: Session = Depends(get_db)
):
    return handlers.add_intake(session=session, intake=intake)


@app.post("/workout", response_model=validators.WorkoutRead, status_code=201)
async def workout_create(
    workout: validators.WorkoutCreate, session: Session = Depends(get_db)
):
    return handlers.add_workout(session=session, workout=workout)
