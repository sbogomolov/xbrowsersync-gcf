import os

def info(request):
    accept_new_syncs = os.environ.get("ACCEPT_NEW_SYNCS", "false")
    status = 1 if accept_new_syncs.lower() == "true" else 3
    return {
        "location": "",
        "maxSyncSize": 512000,
        "message": "",
        "status": status,
        "version": "1.1.13",
    }
