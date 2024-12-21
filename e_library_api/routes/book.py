from fastapi import APIRouter, HTTPException
from models import Book
from typing import List

router = APIRouter()

books_db = []

@router.post("/books/", response_model=Book)
def create_book(book: Book):
    books_db.append(book)
    return book

@router.get("/books/", response_model=List[Book])
def get_books():
    return books_db

@router.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for book in books_db:
        if book.id == book_id:
            book.title = updated_book.title
            book.author = updated_book.author
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@router.delete("/books/{book_id}", response_model=Book)
def delete_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            books_db.remove(book)
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@router.post("/books/{book_id}/unavailable")
def mark_book_unavailable(book_id: int):
    for book in books_db:
        if book.id == book_id:
            book.is_available = False
            return {"message": "Book marked as unavailable"}
    raise HTTPException(status_code=404, detail="Book not found")
