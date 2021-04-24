from typing import Any, Dict

from logic.utils import VERSION, accept_new_syncs


def get_info() -> Dict[str, Any]:
    return {
        "location": "",
        "maxSyncSize": 512000,
        "message": "",
        "status": 1 if accept_new_syncs() else 3,
        "version": VERSION,
    }
