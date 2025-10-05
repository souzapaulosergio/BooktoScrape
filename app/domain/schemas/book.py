from pydantic import BaseModel, Field
from typing import Dict, List
from datetime import datetime

class BookBase(BaseModel):
    categoria: str = Field(..., min_length=1, max_length=50)
    titulo: str = Field(..., min_length=1, max_length=255)
    moeda: str = Field(..., min_length=1, max_length=10)
    preco: float
    rating: int
    estoque: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    #created_at: datetime

    class Config:
        from_attributes = True

class OverviewResponse(BaseModel):
    total_livros: int
    preco_medio: float
    distribuicao_ratings: Dict[int, int]

class CategoryResponse(BaseModel):
    category: str

class CategoryInfo(BaseModel):
    total: int
    prices: List[float]

class StatCategoryResponse(BaseModel):
    total: int
    category: Dict[str, CategoryInfo]