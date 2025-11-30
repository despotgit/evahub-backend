from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import JWT_EXPIRY_INTERVAL

from rest import rest
from test import test
from rest_get import rest_get
from rest_post import rest_post
from rest_put import rest_put
from rest_delete import rest_delete
from auth import auth

import config

app = Flask(__name__)

# Global CORS configuration
CORS(
    app,
    origins=["https://despotovicvladimir.com"],
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_EXPIRY_INTERVAL

jwt = JWTManager(app)

app.secret_key = config.SECRET_KEY

# Register Blueprints
app.register_blueprint(test, url_prefix="/test")
app.register_blueprint(rest, url_prefix="/rest")

app.register_blueprint(rest_get, url_prefix="/rest/get")
app.register_blueprint(rest_post, url_prefix="/rest/post")
app.register_blueprint(rest_put, url_prefix="/rest/put")
app.register_blueprint(rest_delete, url_prefix="/rest/delete")

app.register_blueprint(auth, url_prefix="/auth")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
