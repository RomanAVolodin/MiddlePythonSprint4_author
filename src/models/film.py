from datetime import datetime
from json import JSONEncoder
from uuid import UUID

from pydantic import BaseModel


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, UUID):
            return str(o)  # Convert UUID to string
        elif isinstance(o, datetime):
            return o.isoformat()  # Convert datetime to ISO format string
        return super().default(o)


class Person(BaseModel):
    id: UUID
    name: str


class Genre(BaseModel):
    id: UUID
    name: str

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, obj):
        return cls(**obj)


class Film(BaseModel):
    id: UUID
    title: str
    description: str | None
    imdb_rating: float | None = None
    genres: list[str] = []
    genre: list[Genre] = []
    actors: list[Person] = []
    directors: list[Person] = []
    writers: list[Person] = []
    actors_names: list[str] = []
    directors_names: list[str] = []
    writers_names: list[str] = []
    last_change_date: datetime | None = None

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, obj):
        return cls(**obj)


class Directors(BaseModel):
    id: UUID
    name: str


class Actors(BaseModel):
    id: UUID
    name: str


class Writers(BaseModel):
    id: UUID
    name: str
