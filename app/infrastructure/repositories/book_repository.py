from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from app.domain.entities.books import Book, Users
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
    
    def get_user(self, username: str) -> Optional[Users]:
        return self.db.query(Users).filter(Users.username == username).first()
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.db.query(Book).filter(Book.id == book_id).first()

    def get_by_category(self) -> List[Book]:
        return self.db.query(Book.categoria).distinct().all()
    
    def get_books(self, titulo: Optional[str] = None, categoria: Optional[str] = None) -> List[Book]:
        query = self.db.query(Book)

        if titulo:
            query = query.filter(Book.titulo.ilike(f"%{titulo}%"))
        if categoria:
            query = query.filter(Book.categoria.ilike(f"%{categoria}%"))
        return query.all()
    
    def get_price_range(self,min: float, max = float ) -> List[Book]:
        return (
            self.db.query(Book)
            .filter(Book.preco >= min, Book.preco <= max)
            .all()
        )
    
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
    
    def get_stats_category(self) -> dict:
        total = self.db.query(func.count(Book.id)).scalar()
        
        # Consulta todos os livros agrupados por categoria
        books_by_category = (
            self.db.query(Book.categoria, Book.preco)
            .all()
        )

        category_dict = {}
        for cat, price in books_by_category:
            if cat not in category_dict:
                category_dict[cat] = {"total": 0, "prices": []}
            category_dict[cat]["total"] += 1
            category_dict[cat]["prices"].append(price)

        return {"total": total, "category": category_dict}
    
  
    def get_top_rated(self) -> List[Book]:
        max_rating = self.db.query(func.max(Book.rating)).scalar()
        book = (
                self.db.query(Book)
                .filter(Book.rating == max_rating)
                .all()
                )
        return [
             {
                "id": b.id,
                "categoria": b.categoria,
                "titulo": b.titulo,
                "moeda": b.moeda,
                "preco": b.preco,
                "estoque": b.estoque,
                "rating": b.rating
            } for b in book
        ]
 
