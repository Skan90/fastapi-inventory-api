"""Endpoints da API para o gerenciamento de produtos."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..services import product_service
from ..schemas import product_schema
from ..database import get_db

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", response_model=product_schema.Product, status_code=status.HTTP_201_CREATED)
def create_product(product: product_schema.ProductCreate, db: Session = Depends(get_db)):
    """
    Cria um novo produto no inventário.

    Args:
        product (product_schema.ProductCreate): Os dados do produto a ser criado.
        db (Session): A sessão do banco de dados, injetada pelo FastAPI.

    Returns:
        product_schema.Product: O produto recém-criado, incluindo seu ID.
    """
    return product_service.create_product(db=db, product=product)

@router.get("/", response_model=List[product_schema.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Recupera uma lista de todos os produtos com paginação.

    Args:
        skip (int): O número de produtos a pular.
        limit (int): O número máximo de produtos a retornar.
        db (Session): A sessão do banco de dados, injetada pelo FastAPI.

    Returns:
        List[product_schema.Product]: Uma lista de objetos de produto.
    """
    products = product_service.get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=product_schema.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Recupera um produto específico pelo seu ID.

    Args:
        product_id (int): O ID do produto a ser recuperado.
        db (Session): A sessão do banco de dados, injetada pelo FastAPI.

    Raises:
        HTTPException: Se um produto com o ID fornecido não for encontrado.

    Returns:
        product_schema.Product: O objeto do produto.
    """
    db_product = product_service.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=product_schema.Product)
def update_product(product_id: int, product: product_schema.ProductUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados de um produto existente.

    Args:
        product_id (int): O ID do produto a ser atualizado.
        product (product_schema.ProductUpdate): Os novos dados para o produto.
        db (Session): A sessão do banco de dados, injetada pelo FastAPI.

    Raises:
        HTTPException: Se um produto com o ID fornecido não for encontrado.

    Returns:
        product_schema.Product: O objeto do produto atualizado.
    """
    db_product = product_service.update_product(db=db, product_id=product_id, product_update=product)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return db_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Remove um produto do inventário.

    Args:
        product_id (int): O ID do produto a ser deletado.
        db (Session): A sessão do banco de dados, injetada pelo FastAPI.

    Raises:
        HTTPException: Se um produto com o ID fornecido não for encontrado.
    """
    success = product_service.delete_product(db=db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return None
