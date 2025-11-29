from db_user_documents_broker import deleteUserDocumentFromDb
from common import getUserDocumentsDir

from db_config import getDb
from db import executeCustomQuery

db = getDb()


def addDbUserProject(username, name, description, logs):
    q = (
        "insert into projects "
        + "(`username`,`project_name`,`project_description`,`contained_logs`) "
        + "values ('"
        + username
        + "', '"
        + name[:24]
        + "', '"
        + description
        + "', '"
        + logs
        + "')"
    )

    print("q is:")
    print(q)

    res = executeCustomQuery(q)
    return res


def getUploadedUserProjects(username):
    q = (
        "select project_id, project_name, project_description, contained_logs from projects where username = '"
        + str(username)
        + "'"
    )

    print("q is:" + q)

    results = executeCustomQuery(q)

    toReturn = []
    for r in results:
        toReturn.append(
            {
                "projectId": r[0],
                "projectName": r[1],
                "projectDescription": r[2],
                "projectLogs": r[3],
            }
        )

    # print(toReturn)

    return toReturn


def deleteUserProjectFromDb(username, id):
    deleteUserDocumentFromDb(username, "project", id)
