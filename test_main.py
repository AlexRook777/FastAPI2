from fastapi.testclient import TestClient
import pytest
from main import app, BOOKS

client = TestClient(app)

# Fixture to reset BOOKS data before each test
@pytest.fixture(autouse=True)
def reset_books_data():
    global BOOKS
    BOOKS.clear()
    BOOKS.extend([
        {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925, "rating": 4.2},
        {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960, "rating": 4.5},
        {"id": 3, "title": "1984", "author": "George Orwell", "year": 1949, "rating": 4.8}
    ])

def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_get_book():
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json()["title"] == "The Great Gatsby"

def test_get_book_not_found():
    response = client.get("/books/99")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

def test_search_books_by_rating():
    response = client.get("/books/search/?rating=4.5")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["title"] == "To Kill a Mockingbird"
    assert response.json()[1]["title"] == "1984"


def test_search_books_by_title():
    response = client.get("/books/search/?title=1984")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["author"] == "George Orwell"

def test_search_books_by_author():
    response = client.get("/books/search/?author=George%20Orwell")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "1984"

def test_search_books_by_year():
    response = client.get("/books/search/?year=1960")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "To Kill a Mockingbird"

def test_search_books_combined():
    response = client.get("/books/search/?author=Harper%20Lee&year=1960")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "To Kill a Mockingbird"

def test_search_books_no_results():
    response = client.get("/books/search/?rating=5.0")
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_create_book():
    response = client.post("/books", json={"title": "New Book", "author": "Author", "year": 2023, "rating": 4.0})
    assert response.status_code == 200
    assert response.json()["title"] == "New Book"
    # The id will be 4 because the fixture resets the data
    assert response.json()["id"] == 4

def test_update_book():
    response = client.put("/books/1", json={"title": "Updated Book", "author": "F. Scott Fitzgerald", "year": 1925, "rating": 4.2})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Book"

def test_update_book_not_found():
    response = client.put("/books/99", json={"title": "Updated Book", "author": "F. Scott Fitzgerald", "year": 1925, "rating": 4.2})
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

def test_delete_book():
    response = client.delete("/books/2")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"
    # Verify the book is actually deleted
    get_response = client.get("/books/2")
    assert get_response.status_code == 404

def test_delete_book_not_found():
    response = client.delete("/books/99")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"
