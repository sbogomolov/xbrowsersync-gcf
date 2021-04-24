from flask import Request
from os import environ
from typing import Any, Dict


def info(request: Request) -> Dict[str, Any]:
    accept_new_syncs = environ.get("ACCEPT_NEW_SYNCS", "false")
    status = 1 if accept_new_syncs.lower() == "true" else 3
    return {
        "location": "",
        "maxSyncSize": 512000,
        "message": "",
        "status": status,
        "version": "1.1.13",
    }
