from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import config

from auth import auth
from rest import rest
from rest_get import rest_get
from rest_post import rest_post
from rest_put import rest_put
from rest_delete import rest_delete
from test import test

app = Flask(__name__)

# JWT Configuration
app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.JWT_EXPIRY_INTERVAL
jwt = JWTManager(app)
app.secret_key = config.SECRET_KEY

# -----------------
# Enable CORS globally
# -----------------
# Replace with your actual frontend domain
CORS(app, supports_credentials=True, origins=["https://despotovicvladimir.com"])

# -----------------
# Register blueprints
# -----------------
app.register_blueprint(test, url_prefix="/test")
app.register_blueprint(rest, url_prefix="/rest")
app.register_blueprint(rest_get, url_prefix="/rest/get")
app.register_blueprint(rest_post, url_prefix="/rest/post")
app.register_blueprint(rest_put, url_prefix="/rest/put")
app.register_blueprint(rest_delete, url_prefix="/rest/delete")
app.register_blueprint(auth, url_prefix="/auth")

# -----------------
# Run the app (development only)
# -----------------
if __name__ == "__main__":
    app.run(debug=True)
