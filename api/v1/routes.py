from fastapi import Depends,APIRouter
from data.context import DBContext
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import and_

route = APIRouter(prefix="/api/v1/books", tags=["Books"])

db_context = DBContext()
   
@route.get("/")
async def list_books(db: Session = Depends(db_context.get_db)):
    """
    Endpoint para listar livros coletados.

    Exemplo chama: 
    - **/api/v1/books**
    """    
    db = db_context.SessionLocal()
    books = db.query(db_context.Book).all()
    results = []
    for p in books:
        results.append({
            "id": p.id,
            "categoria": p.categoria,
            "titulo": p.titulo,
            "moeda": p.moeda,
            "preco": p.preco,
            "estoque": p.estoque,
            "rating": p.rating 

        })
    return [{
                "id": b.id,
                "categoria": b.categoria,
                "titulo": b.titulo,
                "moeda": b.moeda,
                "preco": b.preco,
                "estoque": b.estoque,
                "rating": b.rating
            } for b in books
        ]

@route.get("/search")
async def search(
    db: Session = Depends(db_context.get_db),
    titulo: Optional[str] = None,
    categoria: Optional[str] = None
):
    """
    Busca todos os livros filtrando por Titulo e/ou Categoria

    Exemplo de chamada:
    - **/api/v1/books/search?categoria=Sequential Art**
    - **/api/v1/books/search?titulo=Robin War**
    
    Parâmetros:
    - **titulo**: str
    - **categoria**: str
    """

    db = db_context.SessionLocal()
    query = db.query(db_context.Book)

    if titulo:
        query = query.filter(db_context.Book.titulo.ilike(f"%{titulo}%"))
    if categoria:
        query = query.filter(db_context.Book.categoria.ilike(f"%{categoria}%"))

    books = query.all()

    return [
        {
            "id": b.id,
            "categoria": b.categoria,
            "titulo": b.titulo,
            "moeda": b.moeda,
            "preco": b.preco,
            "estoque": b.estoque,
            "rating": b.rating
        } for b in books
    ]    

@route.get("/top-rated")
async def obter_top_rated(
    db: Session = Depends(db_context.get_db)
    ):
    """"""
    db = db_context.SessionLocal()
    max_rating = db.query(func.max(db_context.Book.rating)).scalar()

    books = (
        db.query(db_context.Book)
        .filter(db_context.Book.rating == max_rating)
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
        } for b in books
    ]

@route.get("/price-range")
async def price_range(
        min: float, 
        max: float,  
        db: Session = Depends(db_context.get_db)
    ):
    """
    Busca livros por range de preço
    
    Exemplo de Chamada:
    - ***/api/v1/books/price-range?min=20&max=25***
    
    Parametros: Obrigatórios
    min: float
    max: float
    """

    db = db_context.SessionLocal()
    query = db.query(db_context.Book)

    condicoes = []
    if min is not None:
        condicoes.append(db_context.Book.preco>=min)
    if max is not None:
        condicoes.append(db_context.Book.preco <= max)

    if condicoes:
        query = query.filter(and_(*condicoes))

    books = query.all()

    return [
        {
            "id": b.id,
            "categoria": b.categoria,
            "titulo": b.titulo,
            "moeda": b.moeda,
            "preco": b.preco,
            "estoque": b.estoque,
            "rating": b.rating
        } for b in books
    ]

@route.get("/{book_id}")
async def list_book_details(
        book_id: int, 
        db: Session = Depends(db_context.get_db)
        ):
    """
    Busca de detalhes de livros

    Parametro:
        id: int

    Exemplo chamada:
        **/api/v1/books/1**
    """
    db = db_context.SessionLocal()
    books = db.query(db_context.Book).filter(db_context.Book.id == book_id).first()
    db.close()
    if books:
        return {
                "id": books.id,
                "categoria": books.categoria,
                "titulo": books.titulo,
                "moeda": books.moeda,
                "preco": books.preco,
                "estoque": books.estoque,
                "rating": books.rating
            }  

