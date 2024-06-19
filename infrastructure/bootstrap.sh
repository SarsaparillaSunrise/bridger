#!/usr/bin/bash

if [[ -f db.sqlite3 ]]; then
  echo "DB exists, skipping"
else
  # src/backend/services/seed_db.py
  echo "Bootstrapping DB and loading fixtures..."
  PYTHONPATH=".:" python services/seed_db.py
  echo "DB Initialised"
fi

exec "$@"
