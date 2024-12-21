from fastapi import APIRouter, HTTPException
from models import BorrowRecord, Book, User
from datetime import date
from typing import List  # Import List for type hinting

router = APIRouter()

borrow_records_db = []
books_db = []  # Assume this comes from the Book endpoints
users_db = []  # Assume this comes from the User endpoints

@router.post("/borrow/{user_id}/{book_id}")
def borrow_book(user_id: int, book_id: int):
    user = next((u for u in users_db if u.id == user_id and u.is_active), None)
    if not user:
        raise HTTPException(status_code=400, detail="User not found or inactive")
    
    book = next((b for b in books_db if b.id == book_id and b.is_available), None)
    if not book:
        raise HTTPException(status_code=400, detail="Book is unavailable")
    
    borrow_record = BorrowRecord(
        id=len(borrow_records_db) + 1,
        user_id=user_id,
        book_id=book_id,
        borrow_date=date.today()
    )
    borrow_records_db.append(borrow_record)
    book.is_available = False
    return borrow_record

@router.post("/return/{user_id}/{book_id}")
def return_book(user_id: int, book_id: int):
    record = next((r for r in borrow_records_db if r.user_id == user_id and r.book_id == book_id and r.return_date is None), None)
    if not record:
        raise HTTPException(status_code=400, detail="No active borrow record found")

    record.return_date = date.today()
    book = next(b for b in books_db if b.id == book_id)
    book.is_available = True
    return {"message": "Book returned successfully"}

@router.get("/borrow/{user_id}", response_model=List[BorrowRecord])
def get_user_borrowing_records(user_id: int):
    return [r for r in borrow_records_db if r.user_id == user_id]

@router.get("/borrow", response_model=List[BorrowRecord])
def get_all_borrowing_records():
    return borrow_records_db
