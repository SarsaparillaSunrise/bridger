from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

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
