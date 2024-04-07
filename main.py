from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, joinedload

import schemas
import db
from db import Genre, Book
from dependencies import get_db

SessionLocal = db.SessionLocal
engine = db.engine

db.Base.metadata.create_all(bind=engine)

app = FastAPI()


# CRUD
@app.get("/books/")
def get_books(search: str | None = None, session: Session = Depends(get_db)):
    """ Get all books """
    if search:
        books = session.query(Book).filter(Book.title.ilike(f"%{search}%") | Book.author.ilike(f"%{search}%")).all()
    else:
        books = session.query(Book).all()
    return books


@app.get("/genres/")
def get_genres(session: Session = Depends(get_db)):
    """ Get all genres """
    genres = session.query(Genre).options(joinedload(Genre.books)).all()
    return genres


@app.post("/books/")
def create_book(book: schemas.BookCreate, session: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@app.get("/books/{book_id}")
def read_book(book_id: int, session: Session = Depends(get_db)):
    book = session.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}")
def update_book(book_id: int, book: schemas.BookCreate, session: Session = Depends(get_db)):
    db_book = session.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for var, value in vars(book).items():
        setattr(db_book, var, value)
    session.commit()
    session.refresh(db_book)
    return db_book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, session: Session = Depends(get_db)):
    book = session.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"message": "Book deleted successfully"}


@app.post("/genres/")
def create_genre(genre: schemas.GenreCreate, session: Session = Depends(get_db)):
    db_genre = Genre(**genre.dict())
    session.add(db_genre)
    session.commit()
    session.refresh(db_genre)
    return db_genre


@app.get("/genres/{genre_id}")
def read_genre(genre_id: int, session: Session = Depends(get_db)):
    genre = session.query(Genre).filter(Genre.id == genre_id).first()
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre


@app.put("/genres/{genre_id}")
def update_genre(genre_id: int, genre: schemas.GenreCreate, session: Session = Depends(get_db)):
    db_genre = session.query(Genre).filter(Genre.id == genre_id).first()
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    for var, value in vars(genre).items():
        setattr(db_genre, var, value)
    session.commit()
    session.refresh(db_genre)
    return db_genre


@app.delete("/genres/{genre_id}")
def delete_genre(genre_id: int, session: Session = Depends(get_db)):
    genre = session.query(Genre).filter(Genre.id == genre_id).first()
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    session.delete(genre)
    session.commit()
    return {"message": "Genre deleted successfully"}
