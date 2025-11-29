from flask import Blueprint, request, Response, send_from_directory
from flask_jwt_extended import jwt_required
import requests
import config

rest = Blueprint("rest", __name__)


if False:  # DEV: for testing purposes don't do this check

    @rest.before_request
    @jwt_required(locations=["headers"])
    def before_request():
        print(
            "************************************************* in rest in before_request"
        )
        pass


@rest.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy(path):
    print("********************************************************** in proxy")
    # print(request.__dict__.items())
    mimetype = request.mimetype
    protocol = "https"
    if config.FLASK_ENV == "dev":
        protocol = "http"
    print(f"Before: {request.url}", flush=True)
    url = (
        protocol
        + "://"
        + config.API_TARGET_PATH
        + "/"
        + path
        # + "?"
        # + request.query_string.decode("utf-8")
    )
    print(f"After: {url}", flush=True)
    if request.method == "GET":
        r = requests.get(
            url + f'?{request.query_string.decode("utf-8")}',
            headers={"Authorization": request.headers["Authorization"]},
        )

    if request.method == "POST":
        r = requests.post(
            url,
            data=request.data,
            headers={"Authorization": request.headers["Authorization"]},
        )

    if request.method == "PUT":
        r = requests.put(
            url,
            data=request.data,
            headers={"Authorization": request.headers["Authorization"]},
        )

    if request.method == "DELETE":
        r = requests.delete(
            url,
            data=request.data,
            headers={"Authorization": request.headers["Authorization"]},
        )

    return Response(r.content, mimetype=mimetype)
