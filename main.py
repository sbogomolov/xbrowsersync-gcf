from firebase_admin import firestore
from flask import Request
from google.cloud import runtimeconfig
from os import environ
from typing import Any, Dict
import firebase_admin


VERSION = "1.1.13"

runtime_config_client = runtimeconfig.Client()
config = runtime_config_client.config(environ.get("RUNTIME_CONFIG_NAME"))
accept_new_syncs = config.get_variable("accept_new_syncs")
ACCEPT_NEW_SYNCS = True if accept_new_syncs and accept_new_syncs.text.lower() == "true" else False

firebase_admin.initialize_app()
db = firestore.client()


def info(request: Request) -> Dict[str, Any]:
    status = 1 if ACCEPT_NEW_SYNCS else 3
    return {
        "location": "",
        "maxSyncSize": 512000,
        "message": "",
        "status": status,
        "version": VERSION,
    }
