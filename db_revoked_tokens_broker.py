# import pymongo

import config
from db_config import getDb

db = getDb()


def addRevokedToken(username, jwt, t):
    usersCollection = db["users"]

    t = {"username": username, "is-revoked-token": True, "jwt": jwt, "revoked-at": t}

    # Only add to list of revoked tokens if not added already, no need for duplicates
    if isTokenRevoked(username, jwt):
        return "ok"
    else:
        usersCollection.insert_one(t)
        return "ok"


def isTokenRevoked(username, jwt):
    uc = db["users"]
    token = uc.find_one({"username": username, "is-revoked-token": True, "jwt": jwt})

    if token == None:
        return False
    else:
        return True


def getAllUserRevokedTokensDb(username=None):
    uc = db["users"]

    if None == username:
        revokedTokens = uc.find({"is-revoked-token": True})
    else:
        revokedTokens = uc.find({"username": username, "is-revoked-token": True})

    tokens = []
    if revokedTokens == None:
        print("no revoked tokens")
    else:
        for token in revokedTokens:
            tokens.append(token["jwt"])
    return tokens
