from typing import List
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.domain.schemas.book import BookResponse
from app.application.services.book_service import BookService
from app.infrastructure.repositories.book_repository import BookRepository

router = APIRouter(prefix="/books", tags=["Books"])
router_scrape = APIRouter(tags=["Scrape"])

def get_book_services(db: Session = Depends(get_db)):
    repository = BookRepository(db)
    return BookService(repository)

@router.get("", response_model = List[BookResponse])
def get_all_books(
       service: BookService = Depends(get_book_services)
):
    return service.get_all_book()

@router_scrape.get("/bookscraping")
def list_categorias(service: BookService = Depends(get_book_services)):
    return service.scraping()
