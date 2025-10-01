from data.context import DBContext
from scripts.web_scraping import Scraping
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends

db_context = DBContext()
soup = Scraping()

route_categoria = APIRouter(prefix="/api/v1", tags=["Categorias"])

@route_categoria.get("/categorias")
async def list_categorias(db: Session = Depends(db_context.get_db)):
    """
    Busca por Categorias disponível em Estoque

    Exemplo de chamada:
    - **/api/v1/categorias**
    """
    db = db_context.SessionLocal()
    query = db.query(db_context.Book)
    categorias = db.query(db_context.Book.categoria).filter(db_context.Book.estoque.ilike("%In stock%")).distinct().all()
    db.close()
    return [cat[0] for cat in categorias]