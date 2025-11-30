import datetime
import time
import bcrypt
from flask import request, Blueprint, jsonify
from flask_jwt_extended import create_access_token, decode_token
from db_config import getDb
from db_users_broker import getDbUser
from db_revoked_tokens_broker import isTokenRevoked
import config

auth = Blueprint("auth", __name__)

# ----------------------------
# Helper to finalize response with proper CORS headers
# ----------------------------
def finalizeResponse(r):
    response = jsonify(r)
    response.headers.add("Access-Control-Allow-Origin", "https://despotovicvladimir.com")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response

# ----------------------------
# Register
# ----------------------------
@auth.route("/register", methods=["POST", "OPTIONS"])
def register():
    if request.method == "OPTIONS":
        return finalizeResponse({})

    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    role = "client"

    encoding = "utf-8"
    passwordEncoded = password.encode(encoding)
    hashed = bcrypt.hashpw(passwordEncoded, bcrypt.gensalt())
    hashedDecoded = hashed.decode(encoding)

    connection = getDb()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (`username`, `password`, `email`, `role`) "
            f"VALUES ('{username}', '{hashedDecoded}', '{email}', '{role}')"
        )
        connection.commit()
    except Exception as e:
        connection.rollback()
        msg = str(e)
        if "Duplicate entry" in msg:
            msg = "User with that username already exists"
        return finalizeResponse({"status": "error", "message": msg})
    finally:
        cursor.close()
        connection.close()

    response = {"status": "ok", "message": "User successfully registered."}
    return finalizeResponse(response)

# ----------------------------
# Login
# ----------------------------
@auth.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return finalizeResponse({})

    o = request.get_json()
    username = o.get("username")
    password = o.get("password")

    connection = getDb()
    cursor = connection.cursor()
    sql = f"SELECT password, role, email FROM users WHERE username='{username}'"
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    if not results:
        response = {"authenticated": False, "status": "Failed", "message": "No user with that username exists."}
        return finalizeResponse(response)

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
            "iat": datetime.datetime.now().timestamp()
        }
    else:
        response = {"authenticated": False, "status": "Failed", "message": "Wrong credentials."}

    return finalizeResponse(response)

# ----------------------------
# Test endpoint
# ----------------------------
@auth.route("/test", methods=["GET", "OPTIONS"])
def getTest():
    if request.method == "OPTIONS":
        return finalizeResponse({})
    r = {"authenticated": True, "status": "ok", "message": "Fine"}
    return finalizeResponse(r)

# ----------------------------
# JWT verification helpers
# ----------------------------
def authenticateJwt(username):
    auth_header = request.headers.get("Authorization")
    jwt_token = auth_header.split(" ")[1] if auth_header else ""

    try:
        decodedToken = decode_token(jwt_token)
    except Exception as e:
        return {"status": "error", "authenticated": False, "message": str(e)}

    if decodedToken["sub"] != username:
        return {"status": "error", "authenticated": False, "message": "Username mismatch."}

    timePassed = time.time() - decodedToken["iat"]
    if timePassed > config.JWT_EXPIRY_INTERVAL:
        return {"status": "error", "authenticated": False, "message": "JWT expired", "expired": True}

    # Optionally check for revoked tokens
    if isTokenRevoked(username, jwt_token):
        return {"status": "error", "authenticated": False, "message": "Token is revoked."}

    return {"status": "ok", "authenticated": True, "decodedToken": decodedToken}

def verifyUser(username):
    authentication = authenticateJwt(username)
    if not authentication["authenticated"]:
        return authentication

    user = getDbUser(username)
    if user is None:
        return {"verified": False, "jwt-authenticated": True, "status": "error", "message": "User not found in DB."}
    return {"verified": True, "jwt-authenticated": True, "status": "ok", "message": "User authenticated and verified."}
