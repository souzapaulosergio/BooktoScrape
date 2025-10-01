from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import datetime
import jwt

class Authorization:
    def __init__(self):
        self.security = HTTPBearer()
        self.JWT_SECRET = "uKjVv1vZcwsEZlS9wHQ0"
        self.JWT_ALGORITHM = "HS256"
        self.JWT_EXP_DELTA_SECONDS = 3600

    # Modelo de login
    class LoginRequest(BaseModel):
        username: str
        password: str

    # Cria token JWT
    def create_token(self, username: str) -> str:
        payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=self.JWT_EXP_DELTA_SECONDS)
        }
        token = jwt.encode(payload, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)
        return token

     # Retorna uma dependencia para validar token
    def get_validate_token_dependency(self):
        def validate_token(credentials: HTTPAuthorizationCredentials = Depends(self.security)):
            token = credentials.credentials
            try:
                payload = jwt.decode(token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM])
                return payload
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token expirado")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Token inválido")
        return validate_token
