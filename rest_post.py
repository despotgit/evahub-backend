from flask import Blueprint, json, request
from flask_jwt_extended import jwt_required
from auth import verifyUser, finalizeResponse
from db_user_projects_broker import addDbUserProject
from db_users_broker import getDbUser, updateDbUser

rest_post = Blueprint("rest_post", __name__)


@rest_post.before_request
@jwt_required(locations=["headers"])
def before_request():
    print(
        "************************************************* in rest_post in before_request"
    )
    pass


# Set user data (by username, field name, and value)
# Will be used on Account page to edit user's data
@rest_post.route("/user/set/<username>", methods=["POST"])
def setUserData(username):
    v = verifyUser(username)
    if not v["verified"]:
        return finalizeResponse(v)

    r = json.loads(request.data.decode("UTF-8"))
    updateDbUser(username, r["field"], r["value"])

    # Return response
    response = {
        "authenticated": True,
        "status": "ok",
        "message": "User updated correctly.",
        "username": username,
    }

    return finalizeResponse(response)


@rest_post.route("/document/document-type/<dt>/username/<username>", methods=["POST"])
def postNewDocument(dt, username):
    v = verifyUser(username)
    if not v["verified"]:
        return finalizeResponse(v)

    r = json.loads(request.data.decode("UTF-8"))

    addDbUserProject(
        username,
        str(r["projectName"]),
        str(r["projectDescription"]),
        str(r["projectLogs"]),
    )

    response = {
        "authenticated": True,
        "status": "ok",
        "message": "Project added correctly.",
        "username": username,
    }

    return finalizeResponse(response)
