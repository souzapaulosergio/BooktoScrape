from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.core.database import init_db
from app.core.logging_config import setup_logging
from app.api.routes import book_routes

setup_logging()
init_db()

app = FastAPI(
    title="Books API",
    version="1.0.0",
    description="API para gerenciamento de livros, incluindo listagem, busca e ranking."
)

app.include_router(book_routes.router, prefix="/api/v1")
app.include_router(book_routes.router_scrape, prefix="/api/v1")
app.include_router(book_routes.router_stats, prefix="/api/v1")
app.include_router(book_routes.routes_categoreis, prefix="/api/v1")

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
async def health():
    return JSONResponse(
        content = {
            "status": "healthy"
        }
    )