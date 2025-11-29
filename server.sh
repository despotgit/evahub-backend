#!/bin/sh
export FLASK_APP=app.py
export FLASK_ENV=dev
export FLASK_DEBUG=1
python3 -m flask run