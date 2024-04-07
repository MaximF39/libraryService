from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    description: str
    genre_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True


class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    pass


class Genre(GenreBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True
