from flask import Flask, request, json, make_response
from flask_jwt_extended import JWTManager
import config

from rest import rest
from test import test
from rest_get import rest_get
from rest_post import rest_post
from rest_put import rest_put
from rest_delete import rest_delete
from auth import auth

app = Flask(__name__)

# -----------------------------
# JWT configuration
# -----------------------------
app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.JWT_EXPIRY_INTERVAL
jwt = JWTManager(app)

# Secret key for sessions / JWT
app.secret_key = config.SECRET_KEY

# -----------------------------
# Register blueprints
# -----------------------------
app.register_blueprint(test, url_prefix="/test")
app.register_blueprint(rest, url_prefix="/rest")
app.register_blueprint(rest_get, url_prefix="/rest/get")
app.register_blueprint(rest_post, url_prefix="/rest/post")
app.register_blueprint(rest_put, url_prefix="/rest/put")
app.register_blueprint(rest_delete, url_prefix="/rest/delete")
app.register_blueprint(auth, url_prefix="/auth")

# -----------------------------
# CORS configuration
# -----------------------------
# Allowed origin: your Angular frontend
ALLOWED_ORIGIN = "https://despotovicvladimir.com"

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGIN
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

# Handle preflight OPTIONS requests globally
@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGIN
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

# -----------------------------
# Run only in dev mode
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
