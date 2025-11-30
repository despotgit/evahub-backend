import datetime
import time
import bcrypt
from flask import request, Blueprint, jsonify
from flask_jwt_extended import create_access_token, decode_token
from db_config import getDb
from db_users_broker import getDbUser

auth = Blueprint("auth", __name__)

# -----------------
# Helpers
# -----------------
def finalizeResponse(r):
    response = jsonify(r)
    # CORS headers, in case some endpoints bypass flask-cors
    response.headers.add("Access-Control-Allow-Origin", "https://despotovicvladimir.com")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response


# -----------------
# JWT Authentication Helpers
# -----------------
def authenticateJwt(username):
    auth_header = request.headers.get("Authorization")
    if auth_header:
        jwt_token = auth_header.split(" ")[1]
    else:
        jwt_token = ""

    try:
        decodedToken = decode_token(jwt_token)
    except Exception as e:
        return {"status": "error", "authenticated": False, "message": str(e)}

    if decodedToken["sub"] != username:
        return {
            "status": "error",
            "authenticated": False,
            "message": "Username in the JWT token does not match the username being requested.",
        }

    timePassed = time.time() - decodedToken["iat"]

    if timePassed > config.JWT_EXPIRY_INTERVAL:
        return {
            "status": "error",
            "authenticated": False,
            "message": "JWT is expired",
            "expired": True,
        }

    return {"status": "ok", "authenticated": True, "message": "Token verified.", "decodedToken": decodedToken}


def verifyUser(username):
    authentication = authenticateJwt(username)
    if not authentication["authenticated"]:
        return authentication

    user = getDbUser(username)
    if user is None:
        return {
            "verified": False,
            "jwt-authenticated": True,
            "status": "error",
            "message": "User not found in DB.",
        }
    else:
        return {
            "verified": True,
            "jwt-authenticated": True,
            "status": "ok",
            "message": "User is authenticated and verified.",
        }


# -----------------
# Routes
# -----------------
@auth.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    role = "client"

    encoding = "utf-8"
    hashed = bcrypt.hashpw(password.encode(encoding), bcrypt.gensalt()).decode(encoding)

    connection = getDb()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (`username`, `password`, `email`, `role`) VALUES (%s, %s, %s, %s)",
            (username, hashed, email, role),
        )
        connection.commit()
    except Exception as e:
        msg = str(e)
        if "Duplicate entry" in msg:
            msg = "User with that username already exists"
        return finalizeResponse({"status": "error", "message": msg})
    finally:
        cursor.close()
        connection.close()

    return finalizeResponse({"status": "ok", "message": "User successfully registered."})


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    connection = getDb()
    cursor = connection.cursor()
    cursor.execute("SELECT password, role, email FROM users WHERE username=%s", (username,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    if not results:
        return finalizeResponse({"authenticated": False, "status": "Failed", "message": "No user with that username exists."})

    dbPassword, dbRole, email = results[0]

    if bcrypt.checkpw(password.encode("utf-8"), dbPassword.encode("utf-8")):
        accessToken = create_access_token(identity=username, additional_claims={"some": 123})
        response = {
            "authenticated": True,
            "status": "ok",
            "message": "Login successful.",
            "token": accessToken,
            "role": dbRole,
            "username": username,
            "email": email,
            "iat": datetime.datetime.now().timestamp(),
        }
    else:
        response = {"authenticated": False, "status": "Failed", "message": "Wrong credentials."}

    return finalizeResponse(response)


@auth.route("/test", methods=["GET", "OPTIONS"])
def getTest():
    # Always handle OPTIONS preflight
    if request.method == "OPTIONS":
        return finalizeResponse({})
    return finalizeResponse({"authenticated": True, "status": "ok", "message": "Fine"})
