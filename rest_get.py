import os
from flask import Blueprint, json
from flask_jwt_extended import jwt_required
from auth import verifyUser
from auth import finalizeResponse
from db_user_projects_broker import getUploadedUserProjects
from db_user_documents_broker import getUploadedUserDocuments
from db_users_broker import getDbUser

rest_get = Blueprint("rest_get", __name__)


@rest_get.before_request
@jwt_required(locations=["headers"])
def before_request():
    print("************************************ in rest_get in before_request")
    pass


# Get user (by username)
# will be used on Account or Register page for getting the user's data
@rest_get.route("/user/username/<username>", methods=["GET"])
def getUserData(username):
    v = verifyUser(username)
    if not v["verified"]:
        return finalizeResponse(v)

    user = getDbUser(username)

    response = {
        "authenticated": True,
        "status": "ok",
        "user": user,
        "message": "User retrieved successfully",
    }

    return finalizeResponse(response)


# Get user's documents (by username and document type)
@rest_get.route("documents/type/<documentType>/username/<username>", methods=["GET"])
def getUserDocuments(documentType, username):
    v = verifyUser(username)
    if not v["verified"]:
        return finalizeResponse(v)

    if documentType == "project":
        userDocuments = getUploadedUserProjects(username)
    else:
        userDocuments = getUploadedUserDocuments(username, documentType)

    if userDocuments == None:
        print("No documents of given type for the user are found.")

        response = {
            "authenticated": True,
            "status": "ok",
            "message": "No documents of given type found for the user.",
        }
    else:
        response = {
            "authenticated": True,
            "status": "ok",
            "userDocuments": userDocuments,
            "documentType": documentType,
            "message": "Documents retrieved successfully.",
        }

    return finalizeResponse(response)


# Get user (by username)
# will be used on Account or Register page for getting the user's data
@rest_get.route("/trigger-script", methods=["GET"])
def generateReport():
    print("generating....os.cwd is:")
    print(os.getcwd())
    # p = os.getcwd() + "/report_gen_V12.py"
    # "/Applications/MAMP/htdocs/evahub/backend/report_gen_V12.py"

    # os.system('#!/bin/sh python3 main.py')
    os.system("python3 report_gen_V12.py TestUser/JRC_GridStorage  _06_2023")

    response = {
        "status": "ok",
        "message": "Script triggered successfully.",
    }

    return finalizeResponse(response)

    # return exec("python3 report_gen_V11.py TestUser/JRC_GridStorage  _06_2023")
