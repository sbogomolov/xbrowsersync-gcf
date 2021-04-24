from datetime import datetime
from dateutil import tz
from firebase_admin import firestore
from flask import Response
from google.cloud import runtimeconfig
from google.cloud.firestore import DocumentReference
from http import HTTPStatus
from os import environ
from typing import List
import firebase_admin


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


def not_found() -> Response:
    return Response(status=HTTPStatus.NOT_FOUND)


def bad_request(text: str) -> Response:
    return Response(text, status=HTTPStatus.BAD_REQUEST)


def now() -> datetime:
    return datetime.utcnow().replace(tzinfo=tz.UTC)
