from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Person(BaseModel):
    id: UUID
    name: str


class Genre(BaseModel):
    id: UUID
    name: str


class Film(BaseModel):
    id: UUID
    title: str
    description: str | None
    imdb_rating: float | None = None
    genres: list[str] = []
    actors: list[Person] = []
    directors: list[Person] = []
    writers: list[Person] = []
    actors_names: list[str] = []
    directors_names: list[str] = []
    writers_names: list[str] = []
    last_change_date: datetime | None = None


class FilmSummary(BaseModel):
    id: UUID
    title: str
    imdb_rating: float
