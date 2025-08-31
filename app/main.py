"""Arquivo principal da aplicação FastAPI."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import Base, engine
from .routers import product_router


def create_db_and_tables():
    """Cria as tabelas no banco de dados se elas não existirem."""
    Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia os eventos de inicialização e encerramento da aplicação.

    Na inicialização, cria as tabelas do banco de dados. Em um ambiente de
    produção, isso normalmente seria gerenciado por uma ferramenta de migração
    como o Alembic.
    """
    print("INFO:     Criando banco de dados e tabelas...")
    create_db_and_tables()
    yield
    print("INFO:     Aplicação encerrada.")


app = FastAPI(
    title="API de Inventário de Produtos",
    description="Uma API RESTful para gerenciar um inventário de produtos simples.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(product_router.router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raiz que fornece informações sobre a API e links para a documentação.

    Returns:
        dict: Um dicionário com o nome do projeto, versão e os caminhos para a documentação.
    """
    return {
        "project": app.title,
        "version": app.version,
        "docs_url": app.docs_url,
        "redoc_url": app.redoc_url,
    }
