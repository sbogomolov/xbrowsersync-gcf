from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict
from uuid import uuid4

from common.utils import now


@dataclass
class Bookmarks:
    version: str
    id_: str = uuid4().hex
    bookmarks: str = ""
    last_updated: datetime = now()

    @property
    def last_updated_str(self) -> str:
        return self.last_updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return Bookmarks(**data)
