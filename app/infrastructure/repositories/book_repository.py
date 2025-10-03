from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
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
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.db.query(Book).filter(Book.id == book_id).first()

    def get_by_category(self) -> List[Book]:
        return self.db.query(Book).distinct().all()
    
    def get_books(self, titulo: Optional[str] = None, categoria: Optional[str] = None) -> List[Book]:
        query = self.db.query(Book)

        if titulo:
            query = query.filter(Book.titulo.ilike(f"%{titulo}%"))
        if categoria:
            query = query.filter(Book.categoria.ilike(f"%{categoria}%"))
        return query.all()
    
    def get_overview(self) -> List[Book]:
        total = self.db.query(func.count(Book.id)).scalar()
        preco_medio = self.db.query(func.avg(Book.preco)).scalar()
        ratings = (
            self.db.query(Book.rating, func.count(Book.id))
            .group_by(Book.rating)
            .all()
        )
        distribuicao_ratings = {int(r): qtd for r, qtd in ratings}
        
        return {
            "total_livros": total,
            "preco_medio": float(preco_medio) if preco_medio else 0,
            "distribuicao_ratings": distribuicao_ratings
        }

