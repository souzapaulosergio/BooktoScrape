from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from app.core.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    categoria = Column(String, nullable=False)
    titulo = Column(String, nullable=False)
    moeda = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    rating = Column(Integer, nullable=False)
    estoque = Column(String, nullable=False)
    created_at = Column(DateTime, default= datetime.utcnow)