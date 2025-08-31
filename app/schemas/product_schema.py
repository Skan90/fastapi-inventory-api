"""Schemas Pydantic para validação e serialização de dados de produtos."""

from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    """
    Schema Pydantic base para um produto.

    Contém os campos comuns compartilhados entre os diferentes schemas de produto.

    Attributes:
        name (str): O nome do produto.
        description (Optional[str]): Uma breve descrição do produto.
        price (float): O preço do produto.
        quantity (int): A quantidade disponível em estoque.
    """
    name: str = Field(..., min_length=1, max_length=100, example="Smartphone X")
    description: Optional[str] = Field(None, max_length=300, example="Um smartphone de última geração.")
    price: float = Field(..., gt=0, example=2999.99)
    quantity: int = Field(..., ge=0, example=50)

class ProductCreate(ProductBase):
    """
    Schema para a criação de um novo produto. Herda de ProductBase.

    Nenhum campo adicional é necessário para a criação além do que ProductBase define.
    """
    pass

class ProductUpdate(ProductBase):
    """
    Schema para a atualização de um produto existente.

    Todos os campos são opcionais para permitir atualizações parciais.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)

class Product(ProductBase):
    """
    Schema para o retorno de um produto pela API.

    Inclui o 'id' do banco de dados e é configurado para funcionar com modelos
    SQLAlchemy.

    Attributes:
        id (int): O identificador único para o produto.
    """
    id: int

    class Config:
        from_attributes = True
