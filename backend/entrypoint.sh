#!/bin/sh
set -e

echo "Seeding database..."
python -m scripts.seed

echo "Starting server..."
exec python -m uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload
