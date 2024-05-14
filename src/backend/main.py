from fastapi import FastAPI

app = FastAPI()


LIFTS = [
  {
    "id": 1,
    "category": "compound-lift",
    "name": "squat",
  },
  {
    "id": 2,
    "category": "compound-lift",
    "name": "deadlift",
  },
  {
    "id": 3,
    "category": "compound-lift",
    "name": "bench press",
  }
]

CONSUMABLES = [
  {
    "id": 1,
    "category": "beverage",
    "name": "coffee",
  },
  {
    "id": 2,
    "category": "food",
    "name": "pistachio nuts",
  },
  {
    "id": 3,
    "category": "food",
    "name": "toast",
  }
]


@app.get("/intake")
async def intake():
    return CONSUMABLES


@app.get("/exercise")
async def exercise():
    return CONSUMABLES
