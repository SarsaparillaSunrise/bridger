#!/usr/bin/bash

# src/backend/services/seed_db.py
sleep 5
echo "Bootstrapping DB and loading fixtures..."
PYTHONPATH=".:" python -m alembic upgrade head
PYTHONPATH=".:" python services/seed_db.py
echo "DB Initialised"

exec "$@"
