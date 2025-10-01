from scripts.web_scraping import Scraping
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from scripts.authorization import Authorization

auth = Authorization()
route_scraping = APIRouter(prefix="/api/v1", tags=["Scraping"])
validate_token = auth.get_validate_token_dependency() 

soup = Scraping()

def scraping():
    categorias = soup.obter_categorias()
    all_books = []    
    for nome, link in categorias:
        books = soup.obter_livros(nome, link)
        all_books.extend(books)

    return {"status": "Scraping Finalizado", "total_livros": len(all_books)}

@route_scraping.post("/login")
async def login(data: auth.LoginRequest):
    if data.username == "admin" and data.password == "secret":
        token = auth.create_token(data.username)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Credenciais inválidas")


@route_scraping.get("/bookscraping")
async def book_scraping(background_tasks: BackgroundTasks, user: dict = Depends(validate_token)):
    background_tasks.add_task(scraping)
    return {"status": f"Scraping iniciado pelo usuário {user['username']}"}