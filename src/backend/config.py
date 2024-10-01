import os

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/bridger"
)
TEST_DATABASE_URL = DATABASE_URL + "_test"
