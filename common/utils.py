from datetime import datetime, timezone
from firebase_admin import firestore
from flask import Response, Request
from google.cloud import runtimeconfig
from google.cloud.firestore import DocumentReference
from http import HTTPStatus
from os import environ
from pydantic import BaseModel, ValidationError
from typing import List, Type, TypeVar
from uuid import uuid4
import firebase_admin

from common.exceptions import BadRequestException


VERSION = "1.1.13"
COLLECTION = "bookmarks"

runtime_config_client = runtimeconfig.Client()
config = runtime_config_client.config(environ.get("RUNTIME_CONFIG_NAME"))

firebase_admin.initialize_app()
db = firestore.client()

T = TypeVar("T", bound=BaseModel)


def accept_new_syncs() -> bool:
    accept_new_syncs = config.get_variable("accept_new_syncs")
    return True if accept_new_syncs and accept_new_syncs.text.lower() == "true" else False


def get_document(id_: str) -> DocumentReference:
    return db.collection(COLLECTION).document(id_)


def now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


def new_id() -> str:
    return uuid4().hex


def parse_request(request: Request, model_type: Type[T]) -> T:
    request_json = request.get_json(silent=True)
    if not request_json:
        raise BadRequestException("Request body is not a valid JSON")
    try:
        return model_type(**request_json)
    except ValidationError as e:
        raise BadRequestException(f"Bad request: {e}")


def method_not_allowed(allowed_methods: List[str]) -> Response:
    headers = {"Allow": ", ".join(allowed_methods)}
    return Response(status=HTTPStatus.METHOD_NOT_ALLOWED, headers=headers)


def not_found() -> Response:
    return Response(status=HTTPStatus.NOT_FOUND)


def bad_request(text: str) -> Response:
    return Response(f"{text}\n", status=HTTPStatus.BAD_REQUEST)
