import os
from flask import Blueprint, json, request
from flask_jwt_extended import jwt_required
from auth import verifyUser, finalizeResponse
from db_user_documents_broker import addDbUserLog
from db import executeCustomQuery
from common import getDocumentFileInfo

rest_put = Blueprint("rest_put", __name__)

# Log helper
def log_debug(msg):
    log_file = "/home/despot82/debug_upload.log"  # choose a writable path
    with open(log_file, "a") as f:
        f.write(msg + "\n")


@rest_put.before_request
@jwt_required(locations=["headers"])
def before_request():
    print("************************************* in rest_put in before_request")
    pass


# Set user data (by username, field name, and value)
@rest_put.route(
    "/document/document-type/<documentType>/username/<username>", methods=["PUT"]
)
def uploadDocument(documentType, username):
    logging.debug(f"UploadDocument called: type={documentType}, user={username}")

    v = verifyUser(username)
    if not v["verified"]:
        logging.warning(f"User verification failed for {username}")
        return finalizeResponse(v)

    f = request.files["file"]
    logging.debug(f"Received file: {f.filename}")

    secureFilename, userDir, uploadLocation = getDocumentFileInfo(documentType, username, f.filename, True)
    logging.debug(f"secureFilename={secureFilename}, uploadLocation={uploadLocation}")

    if not os.path.isdir(userDir):
        os.mkdir(userDir)
        logging.debug(f"Directory created: {userDir}")
    else:
        logging.debug(f"Directory already exists: {userDir}")

    f.save(uploadLocation)
    logging.info(f"File saved to {uploadLocation}")

    addDbUserLog(secureFilename, username)
    logging.info(f"DB log added for user {username}")

    response = {"authenticated": True, "status": "ok", "message": "File uploaded."}
    logging.debug(f"Response prepared: {response}")

    return finalizeResponse(response)

