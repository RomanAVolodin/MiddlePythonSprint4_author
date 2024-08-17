from pydantic import UUID4, BaseModel


class FilmRoles(BaseModel):
    uuid: UUID4
    roles: list[str]


class Person(BaseModel):
    uuid: UUID4
    full_name: str
    films: list[FilmRoles]

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, obj):
        return cls(**obj)


class PersonFilm(BaseModel):
    id: UUID4
    title: str
    imdb_rating: float | None = None

    def to_dict(self):
        return self.dict()

    @classmethod
    def from_dict(cls, obj):
        return cls(**obj)
