from flask import Request
import re

from logic.bookmarks import (
    get_bookmarks,
    get_bookmarks_last_updated,
    get_bookmarks_version,
    post_bookmarks,
    put_bookmarks,
)
from logic.info import get_info
from common.utils import method_not_allowed, not_found


def info(request: Request):
    if request.method != "GET":
        return method_not_allowed(["GET"])
    return get_info()


def bookmarks(request: Request):
    path = request.path.rstrip("/")
    if not path:
        if request.method != "POST":
            return method_not_allowed(["POST"])
        return post_bookmarks(request)
    else:
        match = re.match(r"/(\w+)$", path)
        if match:
            if request.method == "GET":
                return get_bookmarks(match[1])
            elif request.method == "PUT":
                return put_bookmarks(match[1], request)
            else:
                return method_not_allowed(["GET", "PUT"])

        match = re.match(r"/(\w+)/lastUpdated$", path)
        if match:
            if request.method != "GET":
                return method_not_allowed(["GET"])
            return get_bookmarks_last_updated(match[1])

        match = re.match(r"/(\w+)/version$", path)
        if match:
            if request.method != "GET":
                return method_not_allowed(["GET"])
            return get_bookmarks_version(match[1])

    return not_found()
