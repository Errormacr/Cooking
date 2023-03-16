#!/usr/bin/env sh
alembic upgrade head
cd server
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000