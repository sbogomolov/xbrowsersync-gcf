from http import HTTPStatus
from firebase_admin import firestore
from flask import Response, Request
from google.cloud import runtimeconfig
from os import environ
from typing import Any, Dict
import firebase_admin


VERSION = "1.1.13"

runtime_config_client = runtimeconfig.Client()
config = runtime_config_client.config(environ.get("RUNTIME_CONFIG_NAME"))

firebase_admin.initialize_app()
db = firestore.client()


def accept_new_syncs() -> bool:
    accept_new_syncs = config.get_variable("accept_new_syncs")
    return True if accept_new_syncs and accept_new_syncs.text.lower() == "true" else False


def info(request: Request) -> Dict[str, Any]:
    if request.method != "GET":
        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)

    status = 1 if accept_new_syncs() else 3
    return {
        "location": "",
        "maxSyncSize": 512000,
        "message": "",
        "status": status,
        "version": VERSION,
    }
