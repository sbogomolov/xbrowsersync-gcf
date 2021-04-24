from flask import Request
import re

from logic.bookmarks import get_bookmarks_version, post_bookmarks
from logic.info import get_info
from logic.utils import method_not_allowed, not_found


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
        # match = re.match(r"/(\w+)$", path)
        # if match:
        #     pass
        match = re.match(r"/(\w+)/version$", path)
        if match:
            if request.method != "GET":
                return method_not_allowed(["GET"])
            return get_bookmarks_version(match[1])

    return not_found()
