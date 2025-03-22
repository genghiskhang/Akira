#!/bin/bash

set -e

echo "Initializing database..."
python init_db.py

echo "Starting Gunicorn server..."
exec gunicorn akira:app --workers 4 --worker-class uvicorn.workers.UvicornWorker -b 0.0.0.0:8080