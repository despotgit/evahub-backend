import braintree
from db_users_broker import getDbUser
from flask import request, Blueprint
from db_revoked_tokens_broker import isTokenRevoked
from flask import Blueprint, json, request


braintree = Blueprint("braintree", __name__)

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="4x976q49xzjvd5jg",
        public_key="txjf56czmn9yhbyw",
        private_key="b2a4337db9660aa289e1638ec8740b57",
    )
)


@braintree.route("/client_token", methods=["GET"])
def client_token():
    return gateway.client_token.generate()


@braintree.route("/pay", methods=["GET"])
def pay():
    print("in the beginning of pay method")
    token = getToken()

    response = json.jsonify(
        {"status": "ok", "token": token, "message": "Token retrieved successfully."}
    )

    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


def getToken():
    # pass client_token to your front-end
    client_token = gateway.client_token.generate({"customer_id": "test2"})
    return client_token


def finalizeResponse(r):
    response = json.jsonify(r)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
