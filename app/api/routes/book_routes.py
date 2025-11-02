from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.domain.schemas.book import BookResponse, OverviewResponse,CategoryResponse, StatCategoryResponse
from app.application.services.book_service import BookService
from app.infrastructure.repositories.book_repository import BookRepository
from app.application.services.jwt_service import JWTService

router = APIRouter(prefix="/books", tags=["Books"])
routes_categoreis = APIRouter(tags=["Category"])
router_stats = APIRouter(prefix = "/stats", tags=["Stats"])
router_scrape = APIRouter(tags=["Scrape"])

jwt_service = JWTService()

def get_book_services(db: Session = Depends(get_db)):
    """Injeção de dependencia, cria uma sessão de banco de dados e retorna"""
    repository = BookRepository(db)
    return BookService(repository)

###Rotas de Livos
@router.get("", response_model = List[BookResponse])
def get_all_books(
       service: BookService = Depends(get_book_services)
):
    """
    Obtem lista de Livros

    Exemplo de chamada:
        /api/v1/books
    """
    return service.get_all_book()

@router.get("/top_rated", response_model= List[BookResponse])
def get_top_rated(service: BookService = Depends(get_book_services)):
    """
    Seleciona os livros com maior rating

    Exemplo de chamada:
        *** /api/v1/books/top_rated ***
    """
    return service.get_top_rated()

@router.get("/search",  response_model= List[BookResponse])
def search(
    service: BookService = Depends(get_book_services),
    titulo: Optional[str] = None,
    categoria: Optional[str] = None
):
    """
    Pesquisa livros por titulo e/ou categoria

    Exemplo de chamada:
        GET api/v1/books/search?titulo=Teste&categoria=travel

    paramentros:
        - Titulo
        - Categoria
    """
    return service.get_book_search(titulo=titulo, categoria = categoria)

@router.get("/price-range", response_model= List[BookResponse])
def get_book_price_rage(
    min: float,
    max: float,
    service: BookService = Depends(get_book_services)    
 ):
    """
    Busca livros por range de preço
    
    Exemplo de Chamada:
        ***/api/v1/books/price-range?min=20&max=25***
    
    Parametros: Obrigatórios
        - min: float
        - max: float
    """
    return service.get_price_range(min=min, max=max)

@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    service: BookService = Depends(get_book_services)
    ):
    """
    Busca de detalhes de livros

    Parametro:
        id: int

    Exemplo chamada:
        **/api/v1/books/1**
    """
    return service.get_book(book_id)

# # ### Rotas Categorias

@routes_categoreis.get("/categories", response_model= List[CategoryResponse])
def get_category(
       service: BookService = Depends(get_book_services)
    ):
    """
    Lista Categorias disponíveis
        exemplo de chamada:
            /api/v1/categories
    response:
    [
        {
            "category": "string"
        }
    ]
    """
    return service.get_category()

# # ###Rotas Estatisticas
@router_stats.get("/overview", response_model= OverviewResponse)
def get_stats_overview(service: BookService = Depends(get_book_services)):
    """
    Obtem visão geral das estatisticas
    Exemplo de chamada:
        /api/v1/stats/overview

    response: 
        {
            "total_livros": 0,
            "preco_medio": 0,
            "distribuicao_ratings": {
                "additionalProp1": 0,
                "additionalProp2": 0,
                "additionalProp3": 0
            }
        }
    """
    return service.get_overview()

@router_stats.get("/categories", response_model= StatCategoryResponse)
def get_stats_category(service: BookService = Depends(get_book_services)):
    """
    Obtem estatisticas por categoria
    Exemplo de chamada:
        /api/v1/stats/categories

    response:
        {
            "total": 0,
            "category": {
                "additionalProp1": {
                "total": 0,
                "prices": [
                    0
                ]
                },
                "additionalProp2": {
                "total": 0,
                "prices": [
                    0
                ]
                },
                "additionalProp3": {
                "total": 0,
                "prices": [
                    0
                ]
                }
            }
            }"""
    return service.get_stats_category()

# ###Rota Scraping
@router_scrape.get("/bookscraping")
def get_data_scrape(
    service: BookService = Depends(get_book_services),
    current_user: str = Depends(jwt_service.get_current_user) 
):
    """
    Rota para iniciar o scraping de livros do site Books to Scrape

    Exemplo de chamada:
        /api/v1/scrape/bookscraping

    Requer autenticação com token JWT
    """
    return service.scraping()