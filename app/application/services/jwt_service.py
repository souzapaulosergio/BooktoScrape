from datetime import datetime, timedelta
from typing import Optional
import jwt  # PyJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status

from app.domain.schemas.auth import TokenData
from app.core.config import settings

class JWTService:
    def __init__(self):
        self.secret_key = settings.jwt_secret_key
        self.algorithm = settings.jwt_algorithm
        self.access_token_expire_minutes = settings.jwt_access_token_expire_minutes

    # Função para criar JWT
    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=self.access_token_expire_minutes))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    # Função para decodificar JWT
    def decode_access_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username = payload.get("sub")
            if username is None:
                return None
            return {"username": username}
        except jwt.ExpiredSignatureError:
            print("Token expirado")
            return None
        except jwt.InvalidTokenError:
            print("Token inválido")
            return None
    
    def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        token = credentials.credentials
        return self.decode_access_token(token)