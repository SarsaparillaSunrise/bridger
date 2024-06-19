from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from adapters.orm import metadata, start_mappers
from domain.model import CategoryExercise, Consumable, Exercise

SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)
SessionLocal = sessionmaker(autoflush=True, bind=engine)

metadata.drop_all(bind=engine)
metadata.create_all(bind=engine)
start_mappers()


session = SessionLocal()
print(session.query(Consumable).all())

# With thanks to strengthlog.com

COMPOUND_LIFTS = (
    "Barbell Squat",
    "Deadlift",
    "Bench Press",
    "Incline Bench Press",
    "Decline Bench Press",
    "Close Grip Press",
    "Seated Dumbbell Overhead Press",
    "Barbell Overhead Press",
    "Push Up",
    "Pull Up",
    "Chin Up",
    "Dip",
    "Leg Press",
    "Bulgarian Split Squat",
    "Hack Squat",
    "Romanian Deadlift",
)

ACCESSORY_EXERCISES = (
    "Dumbbell Chest Fly",
    "Standing Cable Chest Fly",
    "Barbell Shrug",
    "Dumbbell Shrug",
    "Straight Arm Lat Pulldown",
    "Triceps Pushdown",
    "Dumbbell Pullover",
    "Lateral Raise",
    "Front Raise",
    "Reverse Dumbbell Fly",
    "Barbell Curl",
    "Dumbbell Curl",
    "Preacher Curl",
    "Barbell Lying Triceps Extension",
    "Dumbbell Triceps Extension",
    "Leg Extension",
    "Leg Curl",
    "Standing Calf Raise",
)


session.add_all(
    Exercise(name=e, category=CategoryExercise.COMPOUND_LIFT) for e in COMPOUND_LIFTS
)
session.add_all(
    Exercise(name=e, category=CategoryExercise.ACCESSORY) for e in ACCESSORY_EXERCISES
)

session.commit()

print("Exercises added")
