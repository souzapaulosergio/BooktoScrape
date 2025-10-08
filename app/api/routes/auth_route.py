from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from app.application.services.jwt_service import JWTService
from app.domain.schemas.auth import UserLogin, Token
from app.application.services.jwt_service import JWTService

router = APIRouter(tags=["Login"])

@router.post("/login", response_model=Token)
def login(user_login: UserLogin):
    """
        Rota de login obter Token de acesso para rota protegida
    """
    jwt_service = JWTService()

    demo_users = {
            "admin": "admin123",
            "user": "user123"
        }

    if user_login.username not in demo_users or demo_users[user_login.username] != user_login.password:
        print("Falha na autenticação")  # <-- debug
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token_expires = timedelta(minutes=60)
    access_token = jwt_service.create_access_token(
        data={"sub": user_login.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

