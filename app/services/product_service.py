"""Lógica de negócio para o tratamento de operações relacionadas a produtos."""

from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import product_model
from ..schemas import product_schema


def get_product(db: Session, product_id: int) -> Optional[product_model.Product]:
    """
    Recupera um único produto do banco de dados pelo seu ID.

    Args:
        db (Session): A sessão do banco de dados.
        product_id (int): O ID do produto a ser recuperado.

    Returns:
        Optional[product_model.Product]: O objeto do produto se encontrado, caso contrário None.
    """
    return db.query(product_model.Product).filter(product_model.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[product_model.Product]:
    """
    Recupera uma lista de produtos do banco de dados com paginação.

    Args:
        db (Session): A sessão do banco de dados.
        skip (int): O número de registros a pular.
        limit (int): O número máximo de registros a retornar.

    Returns:
        List[product_model.Product]: Uma lista de objetos de produto.
    """
    return db.query(product_model.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: product_schema.ProductCreate) -> product_model.Product:
    """
    Cria um novo produto no banco de dados.

    Args:
        db (Session): A sessão do banco de dados.
        product (product_schema.ProductCreate): Os dados do produto a ser criado.

    Returns:
        product_model.Product: O objeto do produto recém-criado.
    """
    db_product = product_model.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product_update: product_schema.ProductUpdate) -> Optional[product_model.Product]:
    """
    Atualiza um produto existente no banco de dados.

    Args:
        db (Session): A sessão do banco de dados.
        product_id (int): O ID do produto a ser atualizado.
        product_update (product_schema.ProductUpdate): Os novos dados para o produto.

    Returns:
        Optional[product_model.Product]: O objeto do produto atualizado, ou None se não for encontrado.
    """
    db_product = get_product(db, product_id)
    if not db_product:
        return None

    update_data = product_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    """
    Deleta um produto do banco de dados.

    Args:
        db (Session): A sessão do banco de dados.
        product_id (int): O ID do produto a ser deletado.

    Returns:
        bool: True se o produto foi deletado com sucesso, False caso contrário.
    """
    db_product = get_product(db, product_id)
    if not db_product:
        return False

    db.delete(db_product)
    db.commit()
    return True
