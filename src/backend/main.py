from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from adapters.orm import start_mappers
from config import DATABASE_URL
from domain import validators
from services import handlers

Base = declarative_base()

app = FastAPI(debug=True)


start_mappers()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        # environ.get("ALLOWED_ORIGIN", ""),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencies:


def get_db():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autoflush=True, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/consumable", response_model=List[validators.ConsumableRead])
async def consumables_list(session: Session = Depends(get_db)):
    return handlers.list_consumables(session=session)


@app.get("/exercise", response_model=List[validators.ExerciseRead])
async def exercise_list(session: Session = Depends(get_db)):
    return handlers.list_exercises_ordered_by_recent_use(session=session)


@app.post("/intake", response_model=validators.IntakeRead, status_code=201)
async def intake_create(
    intake: validators.IntakeCreate, session: Session = Depends(get_db)
):
    try:
        return handlers.add_intake(session=session, intake=intake)
    except handlers.IntegrityException:
        raise HTTPException(status_code=422, detail="Integrity Error")


@app.post("/workout", response_model=validators.WorkoutRead, status_code=201)
async def workout_create(
    workout: validators.WorkoutCreate, session: Session = Depends(get_db)
):
    return handlers.add_workout(session=session, workout=workout)
