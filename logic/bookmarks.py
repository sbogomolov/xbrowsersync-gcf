from flask import Response, Request
from typing import Any, Dict, Union

from logic.utils import bad_request, get_document, not_found
from models.bookmarks import Bookmarks


ResponseType = Union[Response, Dict[str, Any]]


def post_bookmarks(request: Request) -> ResponseType:
    request_json = request.get_json(silent=True)
    if not request_json:
        return bad_request("Request body is empty")

    version = request_json.get("version")
    if not version:
        return bad_request('"version" is not provided')

    bookmarks = Bookmarks(version=version)
    get_document(bookmarks.id_).set(bookmarks.to_dict())

    return {"id": bookmarks.id_, "lastUpdated": bookmarks.last_updated_str, "version": bookmarks.version}


def get_bookmarks_version(id_: str) -> ResponseType:
    doc = get_document(id_).get()
    if not doc.exists:
        return not_found()

    bookmarks = Bookmarks.from_dict(doc.to_dict())
    return {"version": bookmarks.version}
