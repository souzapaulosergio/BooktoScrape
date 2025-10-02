from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.entities.books import Book
from app.domain.schemas.book import BookCreate

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, book: BookCreate):
        db_book = Book(**book.model_dump())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def get_all(self) -> List[Book]:
        return self.db.query(Book).all()