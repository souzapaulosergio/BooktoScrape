import requests
from bs4 import BeautifulSoup
from re import sub
from data.context import DBContext
from urllib.parse import urljoin

class Scraping:
     def __init__(self):
          self.db_context = DBContext()
          self.db_context.create_all()
          self.url = "https://books.toscrape.com/"

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
                    db = self.db_context.SessionLocal()
                    
                    moeda = price[0]
                    price = float(sub(r"[^\d.]", "", price))

                    novo_book = self.db_context.Book(
                    categoria=nome_categoria,
                    titulo=title,
                    moeda = moeda,
                    preco=price,
                    estoque=stock,
                    rating = rating
                    ) 
                    db.add(novo_book)
                    db.commit()
                    db.close()

               next_page = soup.select_one("li.next a")
               if next_page:
                    url = urljoin(url, next_page["href"])
               else:
                    url = None
                    return books