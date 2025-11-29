import time
from common import getUserDocumentsDir
from db_config import getDb
from db import executeCustomQuery
import json

db = getDb()


def addDbUserLog(filename, username):
    res = executeCustomQuery(
        "insert into logs (`log_name`,`log_filename`,`username`) values ('"
        + filename[:25]
        + "', '"
        + filename
        + "', '"
        + username
        + "')"
    )
    return res


def getUploadedUserDocuments(username, documentType):
    tableName = documentType + "s"
    idField = documentType + "_id"
    nameField = documentType + "_name"
    filenameField = documentType + "_filename"

    q = (
        "select "
        + idField
        + ", "
        + nameField
        + ", "
        + filenameField
        + " from "
        + tableName
        + " where username = '"
        + str(username)
        + "'"
    )

    print("q is:" + q)

    results = executeCustomQuery(q)

    toReturn = []
    for r in results:
        dir = getUserDocumentsDir(documentType, username)
        filePath = dir + "/" + r[2]

        content = ""

        with open(filePath, "rb") as f:
            if documentType == "project":
                content = json.load(f)

            if documentType == "log":
                text = f.read()
                content = str(text, "utf-8")

            if documentType == "report":
                content = json.load(f)

        toReturn.append(
            {
                documentType + "Id": r[0],
                documentType + "Name": r[1],
                documentType + "Content": content,
            }
        )

    # print(toReturn)

    return toReturn


def deleteUserDocumentFromDb(username, documentType, id):
    tableName = documentType + "s"
    idField = documentType + "_id"

    dq = (
        "delete from "
        + tableName
        + " where username = '"
        + str(username)
        + "' and "
        + idField
        + " = "
        + id
    )

    # print("query is:")
    # print(dq)

    deleteRes = executeCustomQuery(dq)

    return deleteRes


def getDocumentFilenameFromDb(username, documentType, id):
    tableName = documentType + "s"
    idField = documentType + "_id"
    filenameField = documentType + "_filename"

    sq = (
        "select "
        + filenameField
        + " from "
        + tableName
        + " where username = '"
        + str(username)
        + "' and "
        + idField
        + "="
        + id
    )

    res = executeCustomQuery(sq, True)

    return res
