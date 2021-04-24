from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict
from uuid import uuid4


@dataclass
class Bookmarks:
    version: str
    id_: str = uuid4().hex
    bookmarks: str = ""
    last_updated: datetime = datetime.now()

    @property
    def last_updated_str(self) -> str:
        return f"{self.last_updated.isoformat()}Z"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return Bookmarks(**data)
