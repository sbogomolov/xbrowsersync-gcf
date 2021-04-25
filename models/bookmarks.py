from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict

from common.utils import new_id, now


@dataclass
class Bookmarks:
    version: str
    id_: str = field(default_factory=new_id)
    bookmarks: str = ""
    last_updated: datetime = field(default_factory=now)

    @property
    def last_updated_str(self) -> str:
        return self.last_updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return Bookmarks(**data)
