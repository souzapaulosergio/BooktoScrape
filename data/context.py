from sqlalchemy import create_engine, Column,Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from datetime import datetime

class DBContext():
     def __init__(self):
          """
          Cria o diretório caso não exista e o banco de dados SQlite
          """
          self.data = os.path.join(os.path.dirname(__file__), "..", "data")
          os.makedirs(self.data, exist_ok=True)

          DB_URL = f"sqlite:///{os.path.join(self.data, 'books.db')}"
          self.engine = create_engine(DB_URL, echo=True)

          self.Base = declarative_base()
          self.SessionLocal = sessionmaker(bind=self.engine)     

          class Book(self.Base):
               __tablename__ = 'books'
               id = Column(Integer, primary_key=True, autoincrement=True)
               categoria = Column(String, nullable=False)
               titulo = Column(String, nullable=False)
               moeda = Column(String, nullable=False)
               preco = Column(Float, nullable=False)
               rating = Column(Integer, nullable=False)
               estoque = Column(String, nullable=False)
               create_at = Column(DateTime, default= datetime.utcnow)

          self.Book = Book

     def create_all(self):
        self.Base.metadata.create_all(self.engine)

     def get_db(self):
          db = self.SessionLocal()
          try:
               yield db
          finally:
               db.close()
