from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from app.application.services.jwt_service import JWTService
from app.domain.schemas.auth import UserLogin, Token
from app.infrastructure.repositories.book_repository import BookRepository
from app.core.database import SessionLocal
from sqlalchemy.orm import Session
router = APIRouter(tags=["Login"])

@router.post("/login", response_model=Token)
def login(user_login: UserLogin):
    """
        Rota de login obter Token de acesso para rota protegida
    """
    jwt_service = JWTService()
    db_session = SessionLocal() # Substitua por sua sessão de banco de dados real

    repo = BookRepository(db_session)  # db_session precisa ser criado
    user = repo.get_user(user_login.username)

    if not user or user.password != user_login.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="usuario sem permissão de acesso"
        )
    
    access_token_expires = timedelta(minutes=60)
    access_token = jwt_service.create_access_token(
        data={"sub": user_login.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

