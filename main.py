# from fastapi import FastAPI
# from api.v1.routes import route as route_api
# from api.v1.route_categoria import route_categoria as route_api_categoria
# from api.v1.route_scraping import route_scraping as route_pi_scraping
# from api.v1.stats import route_stats as route_api_stats
# from data.context import DBContext
# from sqlalchemy import text
# import logging
# import time
# from fastapi import Request
# import json
# from datetime import datetime

# logger = logging.getLogger("api-logger")

# db_context = DBContext()

# app = FastAPI(
#     title="Books API",
#     version="1.0.0",
#     description="API para gerenciamento de livros, incluindo listagem, busca e ranking."
# )


# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     idem = f"{request.method} {request.url.path}"
#     start_time = time.time()
#     logger.info(f"request_start: {idem}")
    
#     response = await call_next(request)
    
#     duration = time.time() - start_time
#     logger.info(f"request_end: {idem} status={response.status_code} duration={duration:.4f}s")
#     return response

# class JsonFormatter(logging.Formatter):
#     def format(self, record):
#         return json.dumps({
#             "timestamp": datetime.utcnow().isoformat(),
#             "level": record.levelname,
#             "message": record.getMessage(),
#             "logger": record.name
#         })

# handler = logging.StreamHandler()
# handler.setFormatter(JsonFormatter())
# logging.getLogger().addHandler(handler)
# logging.getLogger().setLevel(logging.INFO)

# app.include_router(route_api)
# app.include_router(route_api_categoria)
# app.include_router(route_pi_scraping)
# app.include_router(route_api_stats)

# @app.get("/api/v1/health", tags=["Health"])
# async def health_check():
#     """
#         Função Health Check        
#         - Efetua uma consulta simples na base de dados para validar se a conexão de OK
#     """
#     try:
#         db = db_context.SessionLocal()
#         db.execute(text("SELECT 1"))
#         db.close()
#         return {"status": "ok", "database": "connected"}
#     except Exception as e:
#         return {"status": "error", "database": str(e)}
    
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