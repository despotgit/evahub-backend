import time
from db import executeCustomQuery

from db_config import getDb

db = getDb()


def addDbUser(u):
    usersCollection = db["users"]

    u = {
        "username": u["uid"],
        "first_name": u["firstName"],
        "last_name": u["lastName"],
        "email": u["email"],
        "domain": u["domain"],
        "created-at": str(time.time()),
    }

    usersCollection.insert_one(u)
    return


def getDbUser(username):
    q = "select * from users where username='" + str(username) + "'"
    results = executeCustomQuery(q, True)

    return results


def updateDbUser(username, field, value):
    usersCollection = db["users"]
    uq = {"username": username}

    user = usersCollection.find_one(uq)
    if user == None:
        return None

    updateParameter = {"$set": {field: value, "modified-at": str(time.time())}}

    usersCollection.update({"username": username}, updateParameter)

    return


def deleteAllDbUserData(username):
    usersCollection = db["users"]
    uq = {"username": username}

    user = usersCollection.delete_many(uq)
    if user == None:
        return None
    else:
        return "ok"
