#!/bin/sh

export FLASK_APP=app.py
export FLASK_ENV=dev

# gunicorn --workers=4 --bind 0.0.0.0:8080 wsgi:app

flask run --host=0.0.0.0 --port=5000
