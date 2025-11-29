from flask import Blueprint, json, request
from auth import verifyUser
from auth import finalizeResponse
from db_user_documents_broker import deleteUserDocumentFromDb, getDocumentFilenameFromDb
from common import getDocumentFileInfo
from file_system_manager import removeFile


rest_delete = Blueprint("rest_delete", __name__)


# Delete a document (by username, and document id)
@rest_delete.route(
    "/document/id/<documentId>/username/<username>/document-type/<documentType>",
    methods=["DELETE"],
)
def deleteDocument(documentId, username, documentType):
    v = verifyUser(username)
    if not v["verified"]:
        return finalizeResponse(v)

    if documentType == "project":
        print("it's a project, so no files to delete")
    else:
        filename = getDocumentFilenameFromDb(username, documentType, documentId)
        _, _, fullFilePath = getDocumentFileInfo(documentType, username, filename[0])
        removeFile(fullFilePath)

    deleteUserDocumentFromDb(username, documentType, documentId)

    # Return response
    response = {
        "authenticated": True,
        "status": "ok",
        "message": "Document with id " + documentId + " is successfully deleted.",
        "username": username,
    }

    return finalizeResponse(response)


# Delete user (by username)
@rest_delete.route("/user/<username>", methods=["DELETE"])
def deleteUser():
    r = {}
    return finalizeResponse(r)
