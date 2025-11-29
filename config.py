import os
from flask import Flask

FLASK_APP = "app.py"
FLASK_ENV = "dev"
LOGIN_EXPIRY_DEV = 3600
LOGIN_EXPIRY_TEST = 3600
LOGIN_EXPIRY_PROD = 3600
SECRET_KEY = "2a43ca5b42240a33dadc64beace65d1f"

if "dev" == FLASK_ENV:
    TARGET_PATH = "http://localhost:5000"
    API_TARGET_PATH = "127.0.0.1:5000/rest"
    # API_TARGET_PATH = "localhost:5000/rest"
    JWT_EXPIRY_INTERVAL = LOGIN_EXPIRY_DEV

if "test" == FLASK_ENV:
    TARGET_PATH = "https://evahub-test.eu"
    API_TARGET_PATH = "evahub-test.eu/evahub-api/evahub/api/v1"
    JWT_EXPIRY_INTERVAL = LOGIN_EXPIRY_TEST

if "production" == FLASK_ENV:
    TARGET_PATH = "https://evahub.eu"
    API_TARGET_PATH = "evahub-test.eu/evahub-api/evahub/api/v1"
    JWT_EXPIRY_INTERVAL = LOGIN_EXPIRY_PROD
