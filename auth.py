import datetime
import time
from db_users_broker import getDbUser
import config
import bcrypt
from flask import request, Blueprint
from db_revoked_tokens_broker import isTokenRevoked
from flask import Blueprint, json, request
from flask_jwt_extended import (
    create_access_token,
    decode_token,
)
from db_config import getDb

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():
    print("in the beginning of it")

    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]
    role = "client"

    print("request.form is:")
    print(request.form)

    print("username is:", username)
    print("password is:", password)

    encoding = "utf-8"
    passwordEncoded = password.encode(encoding)
    hashed = bcrypt.hashpw(passwordEncoded, bcrypt.gensalt())
    hashedDecoded = hashed.decode(encoding)

    connection = getDb()

    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (`username`, `password`, `email`, `role`) VALUES ('"
            + username
            + "', '"
            + hashedDecoded
            + "', '"
            + email
            + "', '"
            + role
            + "')"
        )
    except Exception as e:
        msg = eval(str(e))[1]
        if msg == "Duplicate entry 'a' for key 'username_UNIQUE'":
            msg = "User with that username already exists"

        return {"status": "error", "message": msg}

    # results = cursor.fetchall()
    # for result in results:
    #  print(result[1])

    print("CHECKPOINT 1")

    response = {"status": "ok", "message": "User successfully registered."}

    return finalizeResponse(response)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@auth.route("/login", methods=["POST"])
def login():
    isPostman = False

    if not isPostman:
        print(request.get_json())

        o = request.get_json()

        username = o["username"]
        password = o["password"]
    else:
        username = request.form["username"]
        password = request.form["password"]

    connection = getDb()
    cursor = connection.cursor()
    sql = "SELECT password, role, email FROM users WHERE username='" + username + "'"

    cursor.execute(sql)
    results = cursor.fetchall()

    if results == ():
        msg = "No user with that username exists."
        authenticated = False
        status = "Failed"
    else:
        result = results[0]
        dbPassword = result[0]
        dbRole = result[1]
        email = result[2]

        if bcrypt.checkpw(password.encode("utf-8"), dbPassword.encode("utf-8")):
            # print("It matches!")
            msg = "Login successful."
            authenticated = True
            accessToken = create_access_token(
                identity=username, additional_claims={"some": 123}
            )
            status = "ok"
        else:
            # print("It does not match :(")
            msg = "Wrong credentials."
            authenticated = False
            status = "Failed"

    response = {}
    response["authenticated"] = authenticated
    response["status"] = status
    response["message"] = msg

    if authenticated:
        response["token"] = accessToken
        response["role"] = dbRole
        response["username"] = username
        response["email"] = email
        response["iat"] = datetime.datetime.now().timestamp()

    return finalizeResponse(response)


# GET - Test
@auth.route("/test", methods=["GET"])
def getTest():
    r = {"authenticated": True, "status": "ok", "message": "Fine"}
    return finalizeResponse(r)


# Check if JWT is genuine and belongs to the user for which the resource is requested
# (i.e. the argument "username" has to be the same as the username in JWT)
def authenticateJwt(username):
    auth_header = request.headers.get("Authorization")
    if auth_header:
        jwt_token = auth_header.split(" ")[1]
    else:
        jwt_token = ""

    # Check that token can be properly decoded
    try:
        decodedToken = decode_token(jwt_token)
    except Exception as e:
        print(e)
        return {"status": "error", "authenticated": False, "message": str(e)}

    # print("decodedToken is:")
    # print(decodedToken)

    if decodedToken["sub"] != username:
        return {
            "status": "error",
            "authenticated": False,
            "message": "Username in the JWT token does not match the username being requested.",
        }

    # Check if JWT is not expired
    timePassed = time.time() - decodedToken["iat"]

    # print("timepassed is:")
    # print(timePassed)

    # print("config.JWT_EXPIRY_INTERVAL is:")
    # print(config.JWT_EXPIRY_INTERVAL)

    if timePassed > config.JWT_EXPIRY_INTERVAL:
        return {
            "status": "error",
            "authenticated": False,
            "message": "JWT is expired",
            "expired": True,
        }

    checkIfRevoked = False

    # Check that JWT is not revoked
    if checkIfRevoked and isTokenRevoked(username, jwt_token):
        return {
            "status": "error",
            "authenticated": False,
            "message": "Token is revoked.",
        }
    else:
        # 1. JWT is valid and authenticated,
        # 2. authorized (username parameter is equal from username from JWT),
        # 3. JWT is not expired
        # 4. JWT is not revoked
        return {
            "status": "ok",
            "authenticated": True,
            "message": "Token successfully verified for given user.",
            "decodedToken": decodedToken,
        }


# Verify:
# 1. The given username is equal to the username extracted from the jwt
# 2. User exists in the database
def verifyUser(username):
    authentication = authenticateJwt(username)

    if not authentication["authenticated"]:
        return authentication

    user = getDbUser(username)

    if user == None:
        print("User not found in DB")

        ret = {
            "verified": False,
            "jwt-authenticated": True,
            "status": "error",
            "message": "User not found in DB.",
        }

    else:
        ret = {
            "verified": True,
            "jwt-authenticated": True,
            "status": "ok",
            "message": "User is authenticated and verified.",
        }

    return ret


# Authorization method, based on the decoded token, decide if the user's domain
# is authorized to access that resource
def checkIfAuthorized(decodedToken, resource) -> bool:
    domain = decodedToken["user"]["domain"]

    if domain == "eu.europa.ec":
        isAuthorized = True
    else:
        isAuthorized = False

    # TO DO: Additional checks for the resource in question
    # .....
    print(resource)


def finalizeResponse(r):
    response = json.jsonify(r)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
