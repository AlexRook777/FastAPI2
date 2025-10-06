from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()


# Task 1: Data modeling (Pydantic)
# This class defines the structure of a book with its attributes
class Book(BaseModel):
    title: str
    author: str
    year: int
    rating: float = Field(..., ge=0.0, le=5.0)

# This class extends the Book class and adds an id attribute
class BookResponse(Book):
    id: int

# Task 2: In-memory storage and initialization
# This list stores the books with their attributes
BOOKS = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925, "rating": 4.2},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960, "rating": 4.5},
    {"id": 3, "title": "1984", "author": "George Orwell", "year": 1949, "rating": 4.8}
]

# This variable keeps track of the next available book id
book_id_counter = 4

# Task 3: Reading routes (GET)
# This route returns all books
@app.get("/books", response_model=List[BookResponse])
def get_books():
    return BOOKS

# This route returns a specific book by its id
@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# This route searches for books with a rating greater than or equal to the specified rating
@app.get("/books/search/", response_model=List[BookResponse])
def search_books(
    author: Optional[str] = Query(None, min_length=1),
    title: Optional[str] = Query(None, min_length=1),
    year: Optional[int] = Query(None, gt=0),
    rating: Optional[float] = Query(None, ge=0.0, le=5.0)
):
    result = BOOKS
    if rating is not None:
        result = [book for book in result if book["rating"] >= rating]
    if author:
        result = [
            book for book in result if book["author"].lower() == author.lower()
        ]
    if title:
        result = [
            book for book in result if book["title"].lower() == title.lower()
        ]
    if year:
        result = [book for book in result if book["year"] == year]

    return result

# Task 4: Creating routes (POST)
# This route creates a new book
@app.post("/books", response_model=BookResponse)
def create_book(book: Book):
    global book_id_counter
    book_dict = book.model_dump()
    book_dict["id"] = book_id_counter
    BOOKS.append(book_dict)
    book_id_counter += 1
    return book_dict

# Task 5: Updating routes (PUT)
# This route updates an existing book
@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: Book):
    for i, b in enumerate(BOOKS):
        if b["id"] == book_id:
            book_dict = book.model_dump()
            book_dict["id"] = book_id
            BOOKS[i] = book_dict
            return book_dict
    raise HTTPException(status_code=404, detail="Book not found")

# Task 6: Deleting routes (DELETE)
# This route deletes a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i, b in enumerate(BOOKS):
        if b["id"] == book_id:
            del BOOKS[i]
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
