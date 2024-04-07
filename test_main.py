from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, SQLALCHEMY_DATABASE_URL

# Подготовка тестовой базы данных
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# Функция для получения сессии базы данных для тестов
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Переопределение зависимости get_db для использования тестовой базы данных
app.dependency_overrides[override_get_db] = override_get_db


def create_genre(client):
    genre = client.post("/genres/", json={"name": "Test Genre"}).json()
    return genre


def create_book(client, title="Test Book", author="Test Author", description="test description", genre_id: int = None):
    if not genre_id:
        genre_id = create_genre(client)["id"]
    book = client.post("/books/",
                       json={"title": title,
                             "author": author,
                             "description": description,
                             "genre_id": int(genre_id)}).json()
    return book


def test_create_book():
    client = TestClient(app)
    data = create_book(client, title="Test Book", author="Test Author")
    assert data["title"] == "Test Book"
    assert data["author"] == "Test Author"


def test_read_book():
    client = TestClient(app)
    book = create_book(client, title="Test Book", author="Test Author")
    response = client.get(f"/books/{book['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Test Author"


def test_search_book_by_title():
    client = TestClient(app)
    create_book(client, title="My unique Book", author="Test Author")
    response = client.get(f"/books", params={"search": "My unique Book"})
    assert response.status_code == 200
    data = response.json()[0]
    assert data["title"] == "My unique Book"


def test_search_book_by_author():
    client = TestClient(app)
    create_book(client, title="My Book", author="Test My unique Author")
    response = client.get(f"/books", params={"search": "Test My unique Author"})
    assert response.status_code == 200
    data = response.json()[0]
    assert data["author"] == "Test My unique Author"


def test_update_book():
    client = TestClient(app)
    book = create_book(client)
    genre = create_genre(client)
    response = client.put(f"/books/{book['id']}",
                          json={"title": "Updated Test Book",
                                "author": "Updated Test Author",
                                "description": "test description",
                                "genre_id": genre['id']})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Test Book"
    assert data["author"] == "Updated Test Author"


def test_delete_book():
    client = TestClient(app)
    book = create_book(client)
    response = client.delete(f"/books/{book['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Book deleted successfully"


# Тесты для CRUD операций с жанрами
def test_create_genre():
    client = TestClient(app)
    response = client.post("/genres/", json={"name": "Test Genre"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Genre"


def test_read_genre():
    client = TestClient(app)
    genre = create_genre(client)
    response = client.get(f"/genres/{genre['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Genre"


def test_update_genre():
    client = TestClient(app)
    genre = create_genre(client)
    response = client.put(f"/genres/{genre['id']}", json={"name": "Updated Test Genre"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Test Genre"


def test_delete_genre():
    client = TestClient(app)
    genre = create_genre(client)
    response = client.delete(f"/genres/{genre['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Genre deleted successfully"
