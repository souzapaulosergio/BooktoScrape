from typing import List, Optional
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.domain.schemas.book import BookResponse, OverviewResponse
from app.application.services.book_service import BookService
from app.infrastructure.repositories.book_repository import BookRepository

router = APIRouter(prefix="/books", tags=["Books"])
router_scrape = APIRouter(tags=["Scrape"])
routes_categoreis = APIRouter(tags=["Category"])
router_stats = APIRouter(prefix = "/stats", tags=["Stats"])

def get_book_services(db: Session = Depends(get_db)):
    repository = BookRepository(db)
    return BookService(repository)

@router.get("", response_model = List[BookResponse])
def get_all_books(
       service: BookService = Depends(get_book_services)
):
    return service.get_all_book()

@routes_categoreis.get("/categories", response_model= List[BookResponse])
def get_category(
       service: BookService = Depends(get_book_services)
    ):
    return service.get_category()

@router.get("/search",  response_model= List[BookResponse])
def search(
    service: BookService = Depends(get_book_services),
    titulo: Optional[str] = None,
    categoria: Optional[str] = None
):
    return service.get_book_search(titulo=titulo, categoria = categoria)

@router_stats.get("/overview", response_model= OverviewResponse)
def get_stats_overview(service: BookService = Depends(get_book_services)):
    return service.get_overview()

    
@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    service: BookService = Depends(get_book_services)
    ):
    return service.get_book(book_id)




@router_scrape.get("/bookscraping")
def list_categorias(service: BookService = Depends(get_book_services)):
    return service.scraping()
