
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.infrastructure.repositories.book_repository import BookRepository
from app.application.services.book_service import BookService

# criar sessão do banco manualmente
db: Session = next(get_db())  # get_db é um generator

# criar repositório e serviço manualmente
repository = BookRepository(db)
service = BookService(repository)

# chamar método diretamente
overview = service.get_stats_category()
print(overview)
