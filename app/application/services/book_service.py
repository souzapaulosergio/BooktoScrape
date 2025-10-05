from typing import List, Optional
from fastapi import HTTPException, status
from app.infrastructure.repositories.book_repository import BookRepository
from app.domain.schemas.book import BookResponse, BookCreate, OverviewResponse,CategoryResponse, StatCategoryResponse
from app.domain.entities.books import Book
import requests
from bs4 import BeautifulSoup
from re import sub
from urllib.parse import urljoin

class BookService:
    def __init__(self, reporitory: BookRepository):
        self.repository = reporitory
        self.url = "https://books.toscrape.com/"
    
    def get_all_book(self) -> List[BookResponse]:
        books = self.repository.get_all()
        return [BookResponse.model_validate(book) for book in books]
    
    def get_category(self) -> List[CategoryResponse]:
          db_book = self.repository.get_by_category()
          # Converte para lista de Pydantic
          categories = [CategoryResponse(category=book[0]) for book in db_book]
          return categories
    
    def get_stats_category(self) -> StatCategoryResponse:
          db_book = self.repository.get_stats_category()
          if not db_book:
               raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail="Livro não encontrado"
               )
          return StatCategoryResponse(**db_book)
    
    def get_price_range(self, min: float, max: float) -> List[BookResponse]:
         db_book = self.repository.get_price_range(min=min, max= max)
         return [BookResponse.model_validate(book) for book in db_book]  

    def get_book_search(self, titulo: Optional[str] = None, categoria: Optional[str] = None) -> List[BookResponse]:
        books = self.repository.get_books(titulo=titulo, categoria=categoria)
        return [BookResponse.model_validate(book) for book in books]
    
    def get_overview(self) -> OverviewResponse:
         db_book = self.repository.get_overview()
         if not db_book:
               raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail="Livro não encontrado"
               )
         return OverviewResponse(**db_book) 

    
    def get_top_rated(self) -> List[BookResponse]:
         db_book = self.repository.get_top_rated()
         return [BookResponse.model_validate(book) for book in db_book]
    
    def get_book(self, book_id: int) -> BookResponse:
         db_book = self.repository.get_by_id(book_id)
         if not db_book:
              raise HTTPException(
                   status_code = status.HTTP_404_NOT_FOUND,
                   detail="Livro não encontrado"
              )
         return BookResponse.model_validate(db_book)
       
    def obter_pagina(self, url=None):
          ##obter o html da pagina
          if url is None:
               url = self.url
          response = requests.get(url)
          response.encoding = "utf-8"
          return BeautifulSoup(response.text, "html.parser")
     
    def obter_categorias(self):
          """
          Função: 
           Coleta todas as categorias dos livros
          """
          soup = self.obter_pagina()
          categorias = soup.select("div.side_categories ul li ul li a")
          return [
                    (
                         categoria.get_text(strip=True), 
                         self.url + categoria["href"]
                    ) 
                    for categoria in categorias
                    ]
     
    def obter_livros(self,nome_categoria, url_categoria):
          """Percorrer todas as páginas da categoria e coletar os dados dos livros 
          armazenando em banco de dados SQLite
          """
          books = []
          url = url_categoria

          while url:
               soup = self.obter_pagina(url)
               items = soup.select("article.product_pod")
               ## convert o star-rating para inteiro 
               rating_map = {
                    
                              "One": 1,
                              "Two": 2,
                              "Three": 3,
                              "Four": 4,
                              "Five": 5
                              }

               for item in items:
                    title = item.h3.a["title"]
                    price = item.select_one("p.price_color").get_text(strip=True)
                    stock = item.select_one("p.instock.availability").get_text(strip=True)
                    rating_tag  = item.select_one("p.star-rating")
                    rating = None
                    if rating_tag:
                         classes = rating_tag.get("class", [])
                         for cls in classes:
                              if cls != "star-rating":
                                   rating = rating_map.get(cls, None) 
                                   break

                    books.append({
                         "categoria": nome_categoria,
                         "titulo": title,
                         "preco": price,
                         "estroque": stock,
                         "rating": rating 
                    })
                   
                    moeda = price[0]
                    price = float(sub(r"[^\d.]", "", price))

                    book = BookCreate(
                    categoria=nome_categoria,
                    titulo=title,
                    moeda=moeda,
                    preco=price,
                    rating=rating,
                    estoque=stock
                    )
                    self.repository.create(book)
                    
               next_page = soup.select_one("li.next a")
               if next_page:
                    url = urljoin(url, next_page["href"])
               else:
                    url = None
                    return books
    
    def scraping(self):
        categorias = self.obter_categorias()
        all_books = []    
        for nome, link in categorias:
            books = self.obter_livros(nome, link)
            all_books.extend(books)

        return {"status": "Scraping Finalizado", "total_livros": len(all_books)}
    