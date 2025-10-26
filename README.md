# techchallenge
API de gerenciamento de Livros fornece *endpoints* Restful para gerenciamento de livros, busca de livros por id, categoria, preço, maior avalição. 

** URL Base ** '/api/v1/login'

Estutura de pastas
BooktoScrape/
|    app/
|        |-api/
|            |-v1/
|               |route/
|                   |- __init__.py
|                   |- auth_route.py
|                   |- book_routes.py                   
|            | __init__.py
|        |- aplication/
|            |- service/
|               |- __init__.py
|               |- book_service.py
|               |- jwt_service.py
|            |- __init__.py
|        |-core/
|            |- __init__.py
|            |- config.py
|            |- database.py
|            |- logging_config.py
|        |-domain/
|            |- entities/
|               |- __init__.py
|               |- books.py
|            |- schemas/
|                |- __init__.py
|                |- auth.py
|                |- book.py
|            |- __init__.py
|        |-infrastructure/
|            |- repositories/
|                |- __init__.py
|                |- book_repository.py
|            |. __init__.py 
|    |- venv
|    |- main.py
|    |- README.md
|    |- requirements.txt
|    |- run.py
|    |- vercel.json

Api para gerenciar e consultar livros usando FAST API e sqlalchemy

## Arquitetura
FastApi - framework para criação de endpoints
SqlAlchemy - para manipulação de dados
SQLite - Base de dados

1. Instalação: Clone o repositório:

    git@github.com:souzapaulosergio/BooktoScrape.git

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
    Execução pelo Swagger (http://127.0.0.1:8000/docs)
    
    ***API Web Scraping: efetua o scraping dados no Site Book to scraping e armazena na base de dados SQLite

        Obter token
            ***POST /api/v1/login***
            Headers
            Content-Type: application/json
        Parâmentros:
           {
            "username": "admin",
            "password": "admin123"
            }
        response:
            {
                "access_token": "eyJhbGciOiJIUzI1iIsInR5cCI6I..."
            }

        pegue o access token e inclua na area de Authorize e salve

        ***GET /api/v1/bookscraping*** API de Web Scraping -- Tabela sera carregada com dados do Site https://books.toscrape.com/
            Authorization: Bearer <token>

    request: **GET /api/v1/books***: lista todos os livros 
    response sucesso (200):
    [
        {
            "categoria": "string",
            "titulo": "string",
            "moeda": "string",
            "preco": 0,
            "rating": 0,
            "estoque": "string",
            "created_at": "2025-10-07T23:45:09.217Z",
            "id": 0
        }
        ]

    request: ***GET /api/v1/books/top-rated**: Lista livros com maior rating  
    response sucesso (200):
        [
            {
                "categoria": "string",
                "titulo": "string",
                "moeda": "string",
                "preco": 0,
                "rating": 0,
                "estoque": "string",
                "created_at": "2025-10-07T23:46:07.550Z",
                "id": 0
            }
        ]
    
    request: ***GET /api/v1/books/search?titulo=Scott Pilgrim's Precious Little Life (Scott Pilgrim %231)***: Lista livros pelo Titulo
    response sucesso (200): 
       [
            {
                "categoria": "string",
                "titulo": "string",
                "moeda": "string",
                "preco": 0,
                "rating": 0,
                "estoque": "string",
                "created_at": "2025-10-07T23:47:56.544Z",
                "id": 0
            }
        ]

    request: *** GET /api/v1/books/price-range?min=20&max=30***: Lista usando filtro de preço min e max 
    response sucesso (200): 
        [
            {
                "categoria": "string",
                "titulo": "string",
                "moeda": "string",
                "preco": 0,
                "rating": 0,
                "estoque": "string",
                "created_at": "2025-10-07T23:49:20.729Z",
                "id": 0
            }
        ] 

    request: ***GET /api/v1/books/{book_id}***: lista livros filtrando pelo ID
    response sucesso (200):
           {
                "categoria": "string",
                "titulo": "string",
                "moeda": "string",
                "preco": 0,
                "rating": 0,
                "estoque": "string",
                "created_at": "2025-10-07T23:50:59.672Z",
                "id": 0
            }

    request: ***GET /api/v1/categorias***: lista categorias
    response sucesso (200):
       [
            {
                "category": "string"
            }
        ]


    request: ***GET /api/v1/stats/overview***: lista categorias
    response sucesso (200):
      {
        "total_livros": 0,
        "preco_medio": 0,
        "distribuicao_ratings": {
                "additionalProp1": 0,
                "additionalProp2": 0,
                "additionalProp3": 0
            }
        }

    request: ***GET /api/v1/stats/categories***: lista Estatistica de categorias
    response sucesso (200):
      {
        "total": 0,
        "category": {
            "additionalProp1": {
            "total": 0,
            "prices": [
                0
            ]
            },
            "additionalProp2": {
            "total": 0,
            "prices": [
                0
            ]
            },
            "additionalProp3": {
            "total": 0,
            "prices": [
                0
            ]
            }
        }
        }   

    Request: ***GET /api/health***: verificar se a api esta conectando com a base de dados
    response:
        {
            "status": "healthy"
        }

    