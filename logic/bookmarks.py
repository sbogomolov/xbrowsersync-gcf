from typing import Any, Dict

from common.utils import accept_new_syncs, get_document, new_id, now
from common.exceptions import BadRequestException, NotFoundException
from models.bookmarks import BookmarksModel, BookmarksPatch, Version


def post_bookmarks(version: Version) -> Dict[str, Any]:
    if not accept_new_syncs():
        raise BadRequestException("Server is not accepting new syncs")

    bookmarks = BookmarksModel(id_=new_id(), bookmarks="", last_updated=now(), version=version.version)
    get_document(bookmarks.id_).set(bookmarks.dict())

    return {"id": bookmarks.id_, "lastUpdated": bookmarks.last_updated.isoformat(), "version": bookmarks.version}


def get_bookmarks(id_: str) -> Dict[str, Any]:
    doc = get_document(id_).get()
    if not doc.exists:
        raise NotFoundException()

    bookmarks = BookmarksModel(**doc.to_dict())
    return {
        "bookmarks": bookmarks.bookmarks,
        "lastUpdated": bookmarks.last_updated.isoformat(),
        "version": bookmarks.version,
    }


def put_bookmarks(id_: str, bookmarks_patch: BookmarksPatch) -> Dict[str, Any]:
    doc_ref = get_document(id_)
    doc = doc_ref.get()
    if not doc.exists:
        raise NotFoundException()

    bookmarks = BookmarksModel(**doc.to_dict())
    if bookmarks.last_updated != bookmarks_patch.last_updated:
        raise BadRequestException(
            f"lastUpdated does not match: {bookmarks_patch.last_updated.isoformat()} != {bookmarks.last_updated.isoformat()}"
        )

    bookmarks.bookmarks = bookmarks_patch.bookmarks
    bookmarks.last_updated = now()
    doc_ref.set(bookmarks.dict())

    return {"lastUpdated": bookmarks.last_updated.isoformat()}


def get_bookmarks_last_updated(id_: str) -> Dict[str, Any]:
    doc = get_document(id_).get()
    if not doc.exists:
        raise NotFoundException()

    bookmarks = BookmarksModel(**doc.to_dict())
    return {"lastUpdated": bookmarks.last_updated.isoformat()}


def get_bookmarks_version(id_: str) -> Dict[str, Any]:
    doc = get_document(id_).get()
    if not doc.exists:
        raise NotFoundException()

    bookmarks = BookmarksModel(**doc.to_dict())
    return {"version": bookmarks.version}
