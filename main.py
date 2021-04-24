from http import HTTPStatus
from firebase_admin import DocumentReference, firestore
from flask import Response, Request
from google.cloud import runtimeconfig
from os import environ
from typing import List
import firebase_admin

from models.bookmarks import Bookmarks


VERSION = "1.1.13"
COLLECTION = "bookmarks"

runtime_config_client = runtimeconfig.Client()
config = runtime_config_client.config(environ.get("RUNTIME_CONFIG_NAME"))

firebase_admin.initialize_app()
db = firestore.client()


def accept_new_syncs() -> bool:
    accept_new_syncs = config.get_variable("accept_new_syncs")
    return True if accept_new_syncs and accept_new_syncs.text.lower() == "true" else False


def get_document(id_: str) -> DocumentReference:
    return db.collection(COLLECTION).document(id_)


def method_not_allowed(allowed_methods: List[str]) -> Response:
    headers = {"Allow": ", ".join(allowed_methods)}
    return Response(status=HTTPStatus.METHOD_NOT_ALLOWED, headers=headers)


def bad_request(text: str) -> Response:
    return Response(text, status=HTTPStatus.BAD_REQUEST)


def info(request: Request):
    if request.method != "GET":
        return method_not_allowed(["GET"])

    status = 1 if accept_new_syncs() else 3
    return {"location": "", "maxSyncSize": 512000, "message": "", "status": status, "version": VERSION}


def bookmarks(request: Request):
    if request.method != "POST":
        return method_not_allowed(["POST"])

    request_json = request.get_json(silent=True)
    if not request_json:
        return bad_request("Request body is empty")

    version = request_json.get("version")
    if not version:
        return bad_request('"version" is not provided')

    bookmarks = Bookmarks(version=version)
    get_document(bookmarks.id_).set(bookmarks.to_dict())

    return {"id": bookmarks.id_, "lastUpdated": bookmarks.last_updated_str, "version": bookmarks.version}


def get_bookmarks_version(request: Request):
    if request.method != "GET":
        return method_not_allowed(["GET"])

    request_json = request.get_json(silent=True)
    if not request_json:
        return bad_request("Request body is empty")

    id_ = request_json.get("id")
    if not id_:
        return bad_request('"id" is not provided')

    doc = get_document(id_).get()
    if not doc.exists:
        return bad_request(f'Bookmarks sync with id "{id_}" does not exist')

    return {"version": doc.version}
