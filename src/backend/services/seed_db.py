import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from adapters.orm import metadata, start_mappers
from config import DATABASE_URL
from domain.model import CategoryConsumable, CategoryExercise, Consumable, Exercise

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autoflush=True, bind=engine)
session = SessionLocal()

if not session.query(Exercise).count() == 0:
    sys.exit()

metadata.drop_all(bind=engine)
metadata.create_all(bind=engine)
start_mappers()


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
    "Tricep Pushdown",
    "Dumbbell Pullover",
    "Lateral Raise",
    "Front Raise",
    "Reverse Dumbbell Fly",
    "Barbell Curl",
    "Dumbbell Curl",
    "Preacher Curl",
    "Barbell Lying Tricep Extension",
    "Dumbbell Tricep Extension",
    "Leg Extension",
    "Leg Curl",
    "Standing Calf Raise",
    "Seated Back Row",
)


session.add_all(
    Exercise(name=e, category=CategoryExercise.COMPOUND_LIFT) for e in COMPOUND_LIFTS
)
session.add_all(
    Exercise(name=e, category=CategoryExercise.ACCESSORY) for e in ACCESSORY_EXERCISES
)

session.add(
    Consumable(
        name="Asahi Super Dry",
        category=CategoryConsumable.BEVERAGE,
        calories=41,
        protein=300,
        carbohydrate=2800,
        fat=0,
    )
)

session.add(
    Consumable(
        name="Ribeye Steak",
        category=CategoryConsumable.FOOD,
        calories=280,
        protein=22_000,
        carbohydrate=0,
        fat=20_000,
    )
)
session.commit()

print("Exercises added")
