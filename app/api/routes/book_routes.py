from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.domain.schemas.book import BookResponse, OverviewResponse,CategoryResponse, StatCategoryResponse
from app.application.services.book_service import BookService
from app.infrastructure.repositories.book_repository import BookRepository

router = APIRouter(prefix="/books", tags=["Books"])
routes_categoreis = APIRouter(tags=["Category"])
router_stats = APIRouter(prefix = "/stats", tags=["Stats"])
router_scrape = APIRouter(tags=["Scrape"])

def get_book_services(db: Session = Depends(get_db)):
    repository = BookRepository(db)
    return BookService(repository)

###Rotas de Livos
@router.get("", response_model = List[BookResponse])
def get_all_books(
       service: BookService = Depends(get_book_services)
):
    return service.get_all_book()

@router.get("/top_rated", response_model= List[BookResponse])
def get_top_rated(service: BookService = Depends(get_book_services)):
    return service.get_top_rated()

@router.get("/search",  response_model= List[BookResponse])
def search(
    service: BookService = Depends(get_book_services),
    titulo: Optional[str] = None,
    categoria: Optional[str] = None
):
    return service.get_book_search(titulo=titulo, categoria = categoria)

@router.get("/price-range", response_model= List[BookResponse])
def get_book_price_rage(
    min: float,
    max: float,
    service: BookService = Depends(get_book_services)    
 ):
    return service.get_price_range(min=min, max=max)

@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    service: BookService = Depends(get_book_services)
    ):
    return service.get_book(book_id)

# # ### Rotas Categorias

@routes_categoreis.get("/categories", response_model= List[CategoryResponse])
def get_category(
       service: BookService = Depends(get_book_services)
    ):
    return service.get_category()

# # ###Rotas Estatisticas
@router_stats.get("/overview", response_model= OverviewResponse)
def get_stats_overview(service: BookService = Depends(get_book_services)):
    return service.get_overview()

@router_stats.get("/categories", response_model= StatCategoryResponse)
def get_stats_category(service: BookService = Depends(get_book_services)):
    return service.get_stats_category()

# ###Rota Scraping
@router_scrape.get("/bookscraping")
def get_data_scrape(service: BookService = Depends(get_book_services)):
    return service.scraping()
