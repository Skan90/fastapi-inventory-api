"""Configuração do banco de dados e gerenciamento de sessões para a aplicação."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# The database URL. It points to a SQLite database file inside the 'data'
# directory, which is mounted as a volume for data persistence.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/database.db")

# The SQLAlchemy engine. The `connect_args` are specific to SQLite and
# are required to allow its use in a multi-threaded environment like FastAPI.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependência do FastAPI para obter uma sessão de banco de dados por requisição.

    Fornece uma sessão do SQLAlchemy que é fechada automaticamente após a
    requisição ser finalizada, garantindo o gerenciamento adequado da conexão.

    Yields:
        Session: A sessão do banco de dados SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
