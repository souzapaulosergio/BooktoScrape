from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path
import os
from pydantic import Field

class Settings(BaseSettings):

    # diretório base: pasta core dentro do projeto
    data_dir: Path = Path(__file__).resolve().parent.parent / "core"
    data_dir.mkdir(parents=True, exist_ok=True)

    # banco sqlite
    database_url: str = Field(default_factory=lambda: f"sqlite:///{(Path(__file__).resolve().parent.parent / 'core' / 'books.db')}")
   
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensetive = False

settings = Settings()