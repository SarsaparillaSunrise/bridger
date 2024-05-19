from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from models import Consumable, Exercise, Intake, Workout
from validators import ConsumableRead, ExerciseRead, IntakeCreate, IntakeRead, WorkoutCreate, WorkoutRead


SQLALCHEMY_DATABASE_URL = "sqlite:///./src/backend/db.sqlite3"

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


# Dependencies:

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Data:

def get_record(session, model, record_id):
    return session.query(model).filter(model.id == record_id).first()


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


# Services:

@app.get("/exercise", response_model=List[ExerciseRead])
async def exercise_list(db: Session = Depends(get_db)):
    return db.query(Exercise).all()


@app.get("/consumable", response_model=List[ConsumableRead])
async def consumables_list(db: Session = Depends(get_db)):
    return db.query(Consumable).all()


@app.post("/intake", response_model=IntakeRead, status_code=201)
async def intake_create(intake: IntakeCreate, session: Session = Depends(get_db)):
    consumable = get_record(session=session, model=Consumable, record_id=1)
    data = dict(calories=consumable.calorie_base / 100 * intake.volume, **intake.model_dump())
    return insert_record(session=session, model=Intake, data=data)


@app.post("/workout", response_model=WorkoutRead, status_code=201)
async def workout_create(workout: WorkoutCreate, session: Session = Depends(get_db)):
    return insert_record(session=session, model=Workout, data=workout.model_dump())
