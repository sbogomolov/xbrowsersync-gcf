from datetime import datetime
from pydantic import BaseModel, Field


class Version(BaseModel):
    version: str


class BookmarksPatch(BaseModel):
    bookmarks: str
    last_updated: datetime = Field(..., alias="lastUpdated")


class BookmarksModel(BookmarksPatch, Version):
    id_: str

    class Config:
        allow_population_by_field_name = True
