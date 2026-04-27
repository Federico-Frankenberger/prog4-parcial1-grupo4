from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .producto import Producto
    from .categoria import Categoria


class ProductoCategoria(SQLModel, table=True):
    __tablename__ = "producto_categoria"

    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categoria.id", primary_key=True)
    es_principal: bool = Field(default=False)

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now()),
    )

    producto: Optional["Producto"] = Relationship(back_populates="categorias_link")
    categoria: Optional["Categoria"] = Relationship(back_populates="productos_link")
