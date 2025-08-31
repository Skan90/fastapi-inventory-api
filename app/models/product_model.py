"""Modelo SQLAlchemy para a tabela 'products'."""

from sqlalchemy import Column, Integer, String, Float
from ..database import Base

class Product(Base):
    """
    Representa um produto no inventário.

    Este modelo é mapeado para a tabela 'products' no banco de dados.

    Attributes:
        id (int): A chave primária para o produto.
        name (str): O nome do produto.
        description (str): Uma breve descrição do produto.
        price (float): O preço do produto.
        quantity (int): A quantidade disponível do produto em estoque.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
