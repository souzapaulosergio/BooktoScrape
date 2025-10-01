# techchallenge
API de geenciamento de Livros Books To Scraping, WebScraping, Monitoramento e Estatisticas

Estutura de pastas
techchalenge/
|-api/
|    |-v1
|        |- __init__.py
|        |- route_categoria.py
|        |- route
|        |- route_scraping.py
|-data/
|    |- books.db
|    |- context.py
|-scripts/
|    |-__init__.py
|    |-web_scraping.py
|    |-authorization.py
|-venv
|-main.py
|-requirements.txt
|-README.md

Api para gerenciar e consultar livros usando FAST API e sqlalchemy

## Arquitetura
FastApi - framework para criação de endpoints
SqlAlchemy - para manipulação de dados
SQLite - Base de dados

1. Instalação: Clone o repositório:

    git@github.com:souzapaulosergio/techchallenge.git

2. Criação do ambiente virtual
    python -m venv venv
    ***Ativar ambiente virtual***
    - **Windows** venv/Scripts/activate 
    - **Linux/MAC**: source venv/bin/activate

    pip install -r requirements.txt

3. Executa server
    uviconr main:app -- reload
    base e tabela será criada
   

4. EndPoints
    request: **GET /api/v1/books***: lista todos os livros 
    response sucesso (200):
    [
        {
            "id": 1,
            "categoria": "Travel",
            "titulo": "It's Only the Himalayas",
            "moeda": "£",
            "preco": 45.17,
            "estoque": "In stock",
            "rating": 2
        }
    ]

    request: ***GET /api/v1/books/search?categoria=Sequential Art***: Lista livros filtrando pela categoria
    response sucesso (200):
        [
            {
                "id": 70,
                "categoria": "Sequential Art",
                "titulo": "Scott Pilgrim's Precious Little Life (Scott Pilgrim #1)",
                "moeda": "£",
                "preco": 52.29,
                "estoque": "In stock",
                "rating": 5
            }
        ]

    request: ***GET /api/v1/books/search?titulo=Scott Pilgrim's Precious Little Life (Scott Pilgrim %231)***: Lista livros pelo Titulo
    response sucesso (200): 
        [
            {
                "id": 70,
                "categoria": "Sequential Art",
                "titulo": "Scott Pilgrim's Precious Little Life (Scott Pilgrim #1)",
                "moeda": "£",
                "preco": 52.29,
                "estoque": "In stock",
                "rating": 5
            }
        ]
    request: ***GET /api/v1/books/top-rated**: Lista livros com maior rating  
    response sucesso (200):
        [
            {
                "id": 11,
                "categoria": "Travel",
                "titulo": "1,000 Places to See Before You Die",
                "moeda": "£",
                "preco": 26.08,
                "estoque": "In stock",
                "rating": 5
            }
        ]

    request: *** GET /api/v1/books/price-range?min=20&max=30***: Lista usando filtro de preço min e max 
    response sucesso (200): 
    [
        {
            "id": 9,
            "categoria": "Travel",
            "titulo": "The Road to Little Dribbling: Adventures of an American in Britain (Notes From a Small Island #2)",
            "moeda": "£",
            "preco": 23.21,
            "estoque": "In stock",
            "rating": 1
        }
    ]  
    request: ***GET /api/v1/books/{book_id}***: lista livros filtrando pelo ID
    response sucesso (200):
            {
            "id": 1,
            "categoria": "Travel",
            "titulo": "It's Only the Himalayas",
            "moeda": "£",
            "preco": 45.17,
            "estoque": "In stock",
            "rating": 2
        }
    request: ***GET /api/v1/categorias***: lista categorias
    response sucesso (200):
        [
            "Travel",
            "Mystery",
            "Historical Fiction",
            "Sequential Art",
            "Classics",
            "Philosophy",
            "Romance",
            "Womens Fiction",
            "Fiction"
        ]

    Request: ***GET /api/v1/health***: verificar se a api esta conectando com a base de dados
    response:
        [
            {"status":"ok","database":"connected"}
        ]

    ***API Web Scraping: efetua o scraping dados no Site Book to scraping e armazena na base de dados SQLite
        Obter token
            ***POST /api/v1/login***
            Headers
            Content-Type: application/json
        Parâmentros:
            {
                "username": "admin",
                "password": "secret"
            }
        response:
            {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6I..."
            }

        ***GET /api/v1/bookscraping*** API de Web Scraping -- Tabela sera carregada com dados do Site https://books.toscrape.com/
            Authorization: Bearer <token>