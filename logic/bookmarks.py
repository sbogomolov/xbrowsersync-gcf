from dateutil import parser
from flask import Response, Request
from typing import Any, Dict, Union

from common.utils import bad_request, get_document, not_found, now
from models.bookmarks import Bookmarks


ResponseType = Union[Response, Dict[str, Any]]


def post_bookmarks(request: Request) -> ResponseType:
    request_json = request.get_json(silent=True)
    if not request_json:
        return bad_request("Request body is empty")

    version = request_json.get("version")
    if not version:
        return bad_request('"version" is not provided')

    bookmarks_doc = Bookmarks(version=version)
    get_document(bookmarks_doc.id_).set(bookmarks_doc.to_dict())

    return {"id": bookmarks_doc.id_, "lastUpdated": bookmarks_doc.last_updated_str, "version": bookmarks_doc.version}


def get_bookmarks(id_: str) -> ResponseType:
    doc = get_document(id_).get()
    if not doc.exists:
        return not_found()

    bookmarks = Bookmarks.from_dict(doc.to_dict())
    return {"bookmarks": bookmarks.bookmarks, "lastUpdated": bookmarks.last_updated_str, "version": bookmarks.version}


def put_bookmarks(id_: str, request: Request) -> ResponseType:
    request_json = request.get_json(silent=True)
    if not request_json:
        return bad_request("Request body is empty")

    last_updated_str = request_json.get("lastUpdated")
    if not last_updated_str:
        return bad_request('"lastUpdated" is not provided')
    last_updated = parser.isoparse(last_updated_str)

    bookmarks = request_json.get("bookmarks")
    if not bookmarks:
        return bad_request('"bookmarks" is not provided')

    doc = get_document(id_).get()
    if not doc.exists:
        return not_found()

    bookmarks_doc = Bookmarks.from_dict(doc.to_dict())
    if bookmarks_doc.last_updated != last_updated:
        return bad_request(f"lastUpdated does not match: {last_updated_str} != {bookmarks_doc.last_updated_str}")

    bookmarks_doc.bookmarks = bookmarks
    bookmarks_doc.last_updated = now()
    doc.set(bookmarks_doc.to_dict())

    return {"lastUpdated": bookmarks_doc.last_updated_str}


def get_bookmarks_last_updated(id_: str) -> ResponseType:
    doc = get_document(id_).get()
    if not doc.exists:
        return not_found()

    bookmarks = Bookmarks.from_dict(doc.to_dict())
    return {"lastUpdated": bookmarks.last_updated_str}


def get_bookmarks_version(id_: str) -> ResponseType:
    doc = get_document(id_).get()
    if not doc.exists:
        return not_found()

    bookmarks_doc = Bookmarks.from_dict(doc.to_dict())
    return {"version": bookmarks_doc.version}
