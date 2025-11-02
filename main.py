from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import init_db, get_db
from app.core.logging_config import setup_logging
from app.api.routes import book_routes
from app.api.routes.auth_route import  router as auth_router
from app.api.middleware.logging_middleware import LoggingMiddleware

setup_logging()

app = FastAPI(
    title="Books API",
    version="1.0.0",
    description="API de gerenciamento de Livros fornece endpoints Restful para gerenciamento de livros, busca de livros por id, categoria, preço, maior avalição."
)

@app.on_event("startup")
def startup_event():
    init_db() 

app.add_middleware(LoggingMiddleware)

app.include_router(book_routes.router, prefix="/api/v1")            
app.include_router(book_routes.routes_categoreis, prefix="/api/v1")
app.include_router(book_routes.router_stats, prefix="/api/v1")
app.include_router(book_routes.router_scrape, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1/auth")

@app.on_event("startup")
async def startuo_event():
    init_db

@app.get("/")
async def root():
    return JSONResponse(
        content = {
            "Message" : "Bem vindo ao Book to Scrape",
            "version": "1.0.0",
            "docs": "/docs"
        }
    )

@app.get("/health")
async def health(db: Session = Depends(get_db)):
    """
    Endpoint de verificação de saúde da API e do Banco de Dados
    """
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"

    status = "healthy" if db_status == "ok" else "unhealthy"

    return JSONResponse(
        content={
            "status": status,
            "database": db_status
        }
    )